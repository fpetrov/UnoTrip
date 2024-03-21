from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from states.registration import RegistrationState

router = Router()

@router.message(RegistrationState.waiting_for_age)
async def age_chosen(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer(
        text='Какой город вы проживаете?',
        reply_markup=ReplyKeyboardRemove()
    )

    await state.set_state(RegistrationState.waiting_for_city)
