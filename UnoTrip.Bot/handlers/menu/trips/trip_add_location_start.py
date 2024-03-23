from datetime import datetime

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.menu.states.trip_edit_state import TripEditState
from handlers.menu.trips.filters.date import DateFilter
from keyboards.row_keyboard import make_row_keyboard
from services.backend import BackendService

router = Router()


@router.message(TripEditState.waiting_for_location_start,
                DateFilter())
async def location_start(message: Message,
                         state: FSMContext,
                         date: datetime):

    await message.answer(
        text=f'Начало посещения локации установлено на <b>{date}</b>',
        parse_mode='HTML'
    )

    current_data = await state.get_data()
    location_data = current_data['location_data']
    location_data['start'] = date

    await state.update_data(location_data=location_data)

    await state.set_state(TripEditState.waiting_for_location_end)


@router.message(TripEditState.waiting_for_location_name)
async def location_start_invalid(message: Message):
    await message.answer(
        text='Неверный формат даты. Ожидается формат YYYY-MM-DD'
    )
