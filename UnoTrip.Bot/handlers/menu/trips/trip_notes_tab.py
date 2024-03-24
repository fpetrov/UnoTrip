from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.callback_query(F.data.startswith('trip_notes_tab_'))
async def notes_command(callback: CallbackQuery,
                        state: FSMContext):
    trip = callback.data.split('_')[-1]

    await state.update_data(trip_id=trip)

    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='📋 Список моих заметок',
                                     callback_data='trip_notes_all'))

    builder.row(InlineKeyboardButton(text='➕ Создать заметку',
                                     callback_data=f'trip_add_note_{trip}'))

    builder.row(InlineKeyboardButton(text='🔙 Назад',
                                     callback_data='menu_back'))

    reply = f'👉 Выбери, что ты хочешь сделать'

    await callback.message.answer(reply,
                                  reply_markup=builder.as_markup())

    await callback.answer()
