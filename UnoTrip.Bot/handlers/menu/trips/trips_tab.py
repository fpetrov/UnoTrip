from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.callback_query(F.data == 'menu_trips')
async def trips_command(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='📋 Список моих путешествий',
                                     callback_data='trips_all'))

    builder.row(InlineKeyboardButton(text='➕ Создать путешествие',
                                     callback_data='trips_create'),
                InlineKeyboardButton(text='🗑 Удалить путешествие',
                                     callback_data='trips_delete'))

    builder.row(InlineKeyboardButton(text='🔙 Назад',
                                     callback_data='menu_back'))

    reply = f'👉 Выбери, что ты хочешь сделать'

    await callback.message.answer(reply,
                                  reply_markup=builder.as_markup())

    await callback.answer()
