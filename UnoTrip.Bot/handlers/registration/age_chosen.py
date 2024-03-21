from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from handlers.registration.states.registration import RegistrationState
from handlers.registration.filters.age import AgeFilter

router = Router()


@router.message(RegistrationState.waiting_for_age,
                AgeFilter())
async def age_chosen(message: Message, state: FSMContext):
    await state.update_data(age=message.text)

    await message.answer(
        text='Отлично, теперь введи свой город. Например, Москва',
        reply_markup=ReplyKeyboardRemove()
    )

    await state.set_state(RegistrationState.waiting_for_city)


@router.message(RegistrationState.waiting_for_age)
async def age_chosen_invalid(message: Message, state: FSMContext):
    await message.answer(
        text='Похоже, что вы ввели возраст в неверном формате. Попробуйте ещё раз'
    )
