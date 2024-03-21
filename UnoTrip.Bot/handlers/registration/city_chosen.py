from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from handlers.registration.states.registration import RegistrationState
from handlers.registration.filters.age import AgeFilter

from keyboards.row_keyboard import make_row_keyboard

router = Router()

callback_answers = ['Да', 'Нет']


@router.message(RegistrationState.waiting_for_city,
                F.text.len() > 2,
                ~F.text.lower().in_({'да', 'нет'}))
async def city_chosen(message: Message, state: FSMContext):
    searched_city = 'Москва'

    await message.answer(
        text=f'Твой город {searched_city}. Верно?',
        reply_markup=make_row_keyboard(*['Да', 'Нет'])
    )

    await state.update_data(city=searched_city)

    # await state.set_state(RegistrationState.waiting_for_city)


@router.message(
    RegistrationState.waiting_for_city,
    F.text.lower() == 'да')
async def city_chosen_callback_yes(message: Message, state: FSMContext):
    await state.set_state(RegistrationState.waiting_for_bio)

    await message.answer(
        text='Супер, осталось чуть-чуть. Введи свое описание профиля',
        reply_markup=ReplyKeyboardRemove())


@router.message(
    RegistrationState.waiting_for_city,
    F.text.lower() == 'нет')
async def city_chosen_callback_no(message: Message):
    await message.answer(
        text='Попробуй ввести свой город еще раз, если не получается, то попробуй конкретизировать.\n'
             'Например, добавив страну или регион',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(RegistrationState.waiting_for_age)
async def city_chosen_invalid(message: Message, state: FSMContext):
    await message.answer(
        text='Похоже, что вы ввели возраст в неверном формате. Попробуйте ещё раз'
    )
