from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.message(Command('menu'))
async def menu_command(message: Message):
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='👤 Мой профиль',
                                     callback_data='menu_profile'),
                InlineKeyboardButton(text='🏖 Мои путешествия',
                                     callback_data='menu_trips'),)

    builder.row(InlineKeyboardButton(text='👥 Найти попутчиков',
                                     callback_data='menu_find_companion'))

    builder.row(InlineKeyboardButton(text='⚙️ Настройки',
                                     callback_data='menu_settings'))

    await message.answer(
        text='👉 Выберите то, что вас интересует',
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data == 'menu_back')
async def menu_back(callback: CallbackQuery):
    await menu_command(callback.message)

    await callback.answer()
