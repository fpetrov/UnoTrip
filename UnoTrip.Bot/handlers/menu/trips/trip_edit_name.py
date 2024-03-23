from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.menu.states.trip_edit_state import TripEditState
from services.backend import BackendService

router = Router()


@router.callback_query(F.data.startswith('trip_edit_name_'))
async def trip_edit_name(callback: CallbackQuery,
                         state: FSMContext):
    reply = f'Хорошо, теперь напиши новое название (от 1 до 150 символов)\n'

    trip_id = callback.data.split('_')[-1]

    await state.update_data(trip_id=trip_id)

    await callback.message.answer(reply)

    await callback.answer()

    await state.set_state(TripEditState.waiting_for_name)


@router.message(TripEditState.waiting_for_name,
                F.text.len() >= 1,
                F.text.len() <= 150)
async def trip_name_chosen(message: Message,
                           state: FSMContext,
                           backend: BackendService):
    current_data = await state.get_data()

    await backend.trip_service.change_name(current_data['trip_id'],
                                           message.text)

    await state.set_state(None)

    await message.answer(
        text='Отлично, ты изменил название путешествия',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(TripEditState.waiting_for_name)
async def trip_name_chosen_invalid(message: Message):
    await message.answer(
        text='Похоже, что ты ввел название в неверном формате. Попробуй ещё раз'
    )
