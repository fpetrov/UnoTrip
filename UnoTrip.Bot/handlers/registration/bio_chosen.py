from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from handlers.registration.states.registration import RegistrationState
from services.backend import BackendService

router = Router()


@router.message(RegistrationState.waiting_for_bio,
                F.text.len() >= 1,
                F.text.len() <= 150)
async def bio_chosen(message: Message,
                     state: FSMContext,
                     backend: BackendService):
    await state.update_data(bio=message.text)
    await state.update_data(registered=True)

    current_data = await state.get_data()

    await backend.user_service.register(message.from_user.id,
                                        current_data['bio'],
                                        current_data['city'],
                                        current_data['age'])

    await message.answer(
        text='🎉 Отлично, на этом регистрация закончилась :)\n'
             'Ты всегда можешь открыть меню, вызвав команду /menu',
        reply_markup=ReplyKeyboardRemove()
    )

    await state.set_state(state=None)


@router.message(RegistrationState.waiting_for_bio)
async def bio_chosen_invalid(message: Message):
    await message.answer(
        text='❌ Похоже, что ты ввел описание в неверном формате. Попробуй ещё раз'
    )
