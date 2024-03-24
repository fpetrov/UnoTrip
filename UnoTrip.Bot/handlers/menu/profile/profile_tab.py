from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.backend import BackendService

router = Router()


# @router.message(Command('profile'))
@router.callback_query(F.data == 'menu_profile')
async def profile_command(callback: CallbackQuery,
                          state: FSMContext,
                          backend: BackendService):
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text='Редактировать возраст',
                                     callback_data='profile_edit_age'),
                InlineKeyboardButton(text='Редактировать город',
                                     callback_data='profile_edit_city'),)

    builder.row(InlineKeyboardButton(text='Редактировать описание',
                                     callback_data='profile_edit_bio'))

    builder.row(InlineKeyboardButton(text='🔙 Назад',
                                     callback_data='menu_back'))

    user_data = await backend.user_service.get(callback.from_user.id)

    reply = f'📌 <b>Имя:</b> {callback.from_user.full_name}\n' \
            f'📌 <b>Возраст:</b> {user_data["age"]}\n' \
            f'📍 <b>Город:</b> {user_data["city"]}\n' \
            f'📌 <b>Описание:</b> {user_data["description"]}\n'

    await callback.message.answer(reply,
                                  reply_markup=builder.as_markup(),
                                  parse_mode='HTML')

    await callback.answer()
