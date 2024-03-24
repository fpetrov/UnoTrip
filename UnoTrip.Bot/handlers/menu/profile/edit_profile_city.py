from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.registration.filters.age import AgeFilter
from handlers.menu.states.profile_state import ProfileEditState
from keyboards.row_keyboard import make_row_keyboard
from services.backend import BackendService
from services.open_street_map import OpenStreetMapService

router = Router()


callback_answers = ['да', 'нет']


@router.callback_query(F.data == 'profile_edit_city')
async def profile_edit_age(callback: CallbackQuery,
                           state: FSMContext):
    reply = f'🔍 Хорошо, теперь введи свой новый город\n'

    await callback.message.answer(reply)

    await callback.answer()

    await state.set_state(ProfileEditState.waiting_for_city)


@router.message(ProfileEditState.waiting_for_city,
                F.text.len() > 2,
                ~F.text.lower().in_(callback_answers))
async def city_chosen(message: Message, state: FSMContext, open_street_map: OpenStreetMapService):
    searched_city = await open_street_map.get_route_information(message.text)

    if not searched_city:
        await message.answer(
            text='☹️ Похоже, что ты ввел несуществующий город. Попробуй ещё раз'
        )
        return

    print(*searched_city)

    await message.answer(
        text=f'🤔 Твой город <b>{searched_city[0]}</b>. Верно?',
        parse_mode='HTML',
        reply_markup=make_row_keyboard('Да', 'Нет')
    )

    await state.update_data(city=searched_city[0])


@router.message(
    ProfileEditState.waiting_for_city,
    F.text.lower() == callback_answers[0])
async def city_chosen_callback_yes(message: Message,
                                   state: FSMContext,
                                   backend: BackendService):
    await state.set_state(None)

    current_data = await state.get_data()

    await backend.user_service.update(
        message.from_user.id,
        {
            'city': current_data['city']
        })

    await message.answer(
        text='🎉 Супер, ты изменил свой город',
        reply_markup=ReplyKeyboardRemove())


@router.message(
    ProfileEditState.waiting_for_city,
    F.text.lower() == callback_answers[1])
async def city_chosen_callback_no(message: Message):
    await message.answer(
        text='🤔 Попробуй ввести свой город еще раз, если не получается, то попробуй конкретизировать.\n'
             'Например, добавив страну или регион',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(ProfileEditState.waiting_for_city)
async def city_chosen_invalid(message: Message):
    await message.answer(
        text='❌ Похоже, что ты ввел город в неверном формате. Попробуй ещё раз'
    )
