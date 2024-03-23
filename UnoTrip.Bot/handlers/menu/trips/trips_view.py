from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.menu.states.trips_state import TripsState
from services.backend import BackendService

router = Router()


@router.callback_query(F.data.startswith('trip_view_'))
async def trip_view_query(callback: CallbackQuery,
                          backend: BackendService,
                          state: FSMContext):

    trip_id = callback.data.split('_')[-1]

    trip = await backend.trip_service.get(trip_id)

    reply = (f'Вот информация о путешествии:\n'
             f'<b>Название:</b> {trip["name"]}\n'
             f'<b>Описание:</b> {trip["description"]}\n'
             f'<b>Локации:</b>\n')

    for i, location in enumerate(trip['locations'], start=1):
        reply += f'{i}. {location["name"]} Старт: {location["start"]} Конец: {location["end"]}\n'

    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='✍️ Поменять название',
                                     callback_data=f'trip_edit_name_{trip["uuid"]}'),
                InlineKeyboardButton(text='✍️ Поменять описание',
                                     callback_data=f'trip_edit_description_{trip["uuid"]}'))

    builder.row(InlineKeyboardButton(text='➕ Добавить локацию',
                                     callback_data=f'trip_add_location_{trip["uuid"]}'),
                InlineKeyboardButton(text='🗑 Удалить локацию',
                                     callback_data=f'trip_delete_location_{trip["uuid"]}'))

    builder.row(InlineKeyboardButton(text='👥 Добавить друга',
                                     callback_data='trips_all'),)

    builder.row(InlineKeyboardButton(text='🔙 Назад',
                                     callback_data='menu_trips'))

    await callback.message.answer(reply,
                                  reply_markup=builder.as_markup(),
                                  parse_mode='HTML')

    await callback.answer()
