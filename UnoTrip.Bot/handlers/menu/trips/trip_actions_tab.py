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

router = Router()

callback_answers = ['да', 'нет']


@router.callback_query(F.data.startswith('trip_actions_tab_'))
async def trip_action_tab(callback: CallbackQuery,
                          state: FSMContext,
                          backend: BackendService):
    reply = f'👉 Хорошо, выбери, что хочешь узнать о локации'

    trip_id = callback.data.split('_')[-1]

    await state.update_data(trip_id=trip_id)

    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='⛅️ Прогноз погоды',
                                     callback_data=f'weather_action_{trip_id}'))

    builder.row(InlineKeyboardButton(text='🗽 Достопримечательности',
                                     callback_data=f'hotels_action_{trip_id}'))

    builder.row(InlineKeyboardButton(text='🛎 Подобрать отели',
                                     callback_data=f'hotels_action_{trip_id}'))

    builder.row(InlineKeyboardButton(text='🍜 Кафе и рестораны',
                                     callback_data=f'hotels_action_{trip_id}'))

    builder.row(InlineKeyboardButton(text='🚘 Аренда машины',
                                     callback_data=f'hotels_action_{trip_id}'))

    builder.row(InlineKeyboardButton(text='👥 Найти попутчика',
                                     callback_data=f'hotels_action_{trip_id}'))

    builder.row(InlineKeyboardButton(text='ℹ️ Топ 5 фактов',
                                     callback_data=f'hotels_action_{trip_id}'))

    builder.row(InlineKeyboardButton(text='🤖 Q/A бот',
                                     callback_data=f'hotels_action_{trip_id}'))

    builder.adjust(2)

    await callback.message.answer(
        text=reply,
        reply_markup=builder.as_markup()
    )

    await callback.answer()


@router.callback_query(F.data.startswith('trip_remove_location_with_'))
async def trip_remove_location_with(callback: CallbackQuery,
                                    state: FSMContext,
                                    backend: BackendService):
    location_id = callback.data.split('_')[-1]

    current_data = await state.get_data()

    await backend.trip_service.delete_location(
        current_data['trip_id'], location_id)

    await callback.message.answer(
        text='🎉 Отлично, локация удалена'
    )

    await callback.answer()

    await state.set_state(None)
