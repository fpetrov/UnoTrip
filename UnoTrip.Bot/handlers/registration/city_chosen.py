from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from handlers.registration.states.registration import RegistrationState
from handlers.registration.filters.age import AgeFilter

from keyboards.row_keyboard import make_row_keyboard
from services.open_street_map import OpenStreetMapService

router = Router()

callback_answers = ['да', 'нет']


@router.message(RegistrationState.waiting_for_city,
                F.text.len() > 2,
                ~F.text.lower().in_(callback_answers))
async def city_chosen(message: Message, state: FSMContext, open_street_map: OpenStreetMapService):
    searched_city = await open_street_map.get_route_information(message.text)

    if not searched_city:
        await message.answer(
            text='Похоже, что ты ввел несуществующий город. Попробуй ещё раз'
        )
        return

    print(*searched_city)

    await message.answer(
        text=f'Твой город <b>{searched_city[0]}</b>. Верно?',
        parse_mode='HTML',
        reply_markup=make_row_keyboard('Да', 'Нет')
    )

    await state.update_data(city=searched_city)


@router.message(
    RegistrationState.waiting_for_city,
    F.text.lower() == callback_answers[0])
async def city_chosen_callback_yes(message: Message, state: FSMContext):
    await state.set_state(RegistrationState.waiting_for_bio)

    await message.answer(
        text='Супер, осталось чуть-чуть. Введи свое описание профиля (от 1 до 150 символов):',
        reply_markup=ReplyKeyboardRemove())


@router.message(
    RegistrationState.waiting_for_city,
    F.text.lower() == callback_answers[1])
async def city_chosen_callback_no(message: Message):
    await message.answer(
        text='Попробуй ввести свой город еще раз, если не получается, то попробуй конкретизировать.\n'
             'Например, добавив страну или регион',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(RegistrationState.waiting_for_city)
async def city_chosen_invalid(message: Message):
    await message.answer(
        text='Похоже, что ты ввел город в неверном формате. Попробуй ещё раз'
    )
