from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.menu.states.trip_edit_state import TripEditState
from keyboards.row_keyboard import make_row_keyboard
from services.backend import BackendService
from services.open_street_map import OpenStreetMapService

router = Router()

callback_answers = ['да', 'нет']


@router.callback_query(F.data.startswith('trip_add_location_'))
async def trip_add_location(callback: CallbackQuery,
                            state: FSMContext):
    reply = f'📍 Хорошо, теперь введи адрес локации, желательно вводить его более конкретно\n'

    trip_id = callback.data.split('_')[-1]

    await state.update_data(trip_id=trip_id)

    await callback.message.answer(reply)

    await callback.answer()

    await state.set_state(TripEditState.waiting_for_location_name)


@router.message(TripEditState.waiting_for_location_name,
                F.text.len() > 2,
                ~F.text.lower().in_(callback_answers))
async def location_chosen(message: Message, state: FSMContext, open_street_map: OpenStreetMapService):
    searched_city = await open_street_map.get_route_information(message.text)

    if not searched_city:
        await message.answer(
            text='❌ Похоже, что ты ввел несуществующую локацию. Попробуй ещё раз'
        )
        return

    print(*searched_city)

    await message.answer(
        text=f'🤔 Твоя локация <b>{searched_city[0]}</b>. Верно?',
        parse_mode='HTML',
        reply_markup=make_row_keyboard('Да', 'Нет')
    )

    await state.update_data(location=searched_city)


@router.message(
    TripEditState.waiting_for_location_name,
    F.text.lower() == callback_answers[0])
async def location_chosen_callback_yes(message: Message,
                                       state: FSMContext,
                                       backend: BackendService):
    await state.set_state(None)

    current_data = await state.get_data()

    location = current_data['location']
    location_data = {
        'name': location[0],
        'latitude': location[1],
        'longitude': location[2],
    }

    await state.update_data(location_data=location_data)

    await message.answer(
        text='🎉 Супер, ты указал локацию. Теперь укажи дату начала посещения локации в формате YYYY-MM-DD',
        reply_markup=ReplyKeyboardRemove())

    await state.set_state(TripEditState.waiting_for_location_start)


@router.message(
    TripEditState.waiting_for_location_name,
    F.text.lower() == callback_answers[1])
async def location_chosen_callback_no(message: Message):
    await message.answer(
        text='☹️ Попробуй ввести свою локацию еще раз, если не получается, то попробуй конкретизировать.\n'
             'Например, добавив страну или регион',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(TripEditState.waiting_for_location_name)
async def location_chosen_invalid(message: Message):
    await message.answer(
        text='❌ Похоже, что ты ввел локацию в неверном формате. Попробуй ещё раз'
    )
