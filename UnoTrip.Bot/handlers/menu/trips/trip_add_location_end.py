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


@router.message(TripEditState.waiting_for_location_end,
                DateFilter())
async def location_end(message: Message,
                       state: FSMContext,
                       date: datetime,
                       backend: BackendService):
    await message.answer(
        text=f'Конец посещения локации установлен на <b>{date}</b>',
        parse_mode='HTML'
    )

    current_data = await state.get_data()
    location_data = current_data['location_data']
    location_data['end'] = date

    await state.update_data(location_data=location_data)

    await backend.trip_service.add_location(current_data['trip_id'],
                                            location_data)

    await state.set_state(None)


@router.message(TripEditState.waiting_for_location_name)
async def location_end_invalid(message: Message):
    await message.answer(
        text='Неверный формат даты. Ожидается формат YYYY-MM-DD'
    )
