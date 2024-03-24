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


@router.callback_query(F.data.startswith('trip_add_note_'))
async def trip_add_note(callback: CallbackQuery,
                        state: FSMContext):
    reply = f'Будут ли твои друзья видеть эту заметку?\n'

    trip_id = callback.data.split('_')[-1]

    await state.update_data(trip_id=trip_id)

    await callback.message.answer(reply,
                                  reply_markup=make_row_keyboard('Да', 'Нет'))

    await callback.answer()

    await state.set_state(TripEditState.waiting_for_note_privacy)


@router.message(
    TripEditState.waiting_for_note_privacy,
    F.text.lower() == callback_answers[0])
async def privacy_chosen_callback_yes(message: Message,
                                      state: FSMContext):
    await state.update_data(note_privacy=False)

    await message.answer(
        text='🔓 Твоя заметка будет видна всем, кто находится в путешествии\n'
             'Теперь введи название для заметки',
        reply_markup=ReplyKeyboardRemove()
    )

    await state.set_state(TripEditState.waiting_for_note_name)


@router.message(
    TripEditState.waiting_for_note_privacy,
    F.text.lower() == callback_answers[1])
async def privacy_chosen_callback_no(message: Message,
                                     state: FSMContext):
    await state.update_data(note_privacy=True)

    await message.answer(
        text='🔒 Твоя заметка будет видна только тебе\n'
             'Теперь введи название для заметки',
        reply_markup=ReplyKeyboardRemove()
    )

    await state.set_state(TripEditState.waiting_for_note_name)


@router.message(TripEditState.waiting_for_note_privacy)
async def privacy_chosen_invalid(message: Message):
    await message.answer(
        text='❌ Похоже, что ты ввел ответ в неверном формате. Попробуй ещё раз'
    )
