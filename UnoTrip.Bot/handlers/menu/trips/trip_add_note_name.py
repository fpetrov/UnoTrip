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


@router.message(TripEditState.waiting_for_note_name,
                F.text.len() > 2)
async def name_chosen(message: Message, state: FSMContext):
    await state.update_data(note_name=message.text)

    await message.answer(
        text=f'Отлично, теперь пришли файл, который хочешь сохранить. Это может быть документ, фотография или видео,'
             f' а может ты хочешь сохранить кружок или даже голосовое сообщение',
    )

    await state.set_state(TripEditState.waiting_for_note_file)


@router.message(TripEditState.waiting_for_note_name)
async def name_chosen_invalid(message: Message):
    await message.answer(
        text='❌ Похоже, что ты ввел название в неверном формате. Попробуй ещё раз'
    )
