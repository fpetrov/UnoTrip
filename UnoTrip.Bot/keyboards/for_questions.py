from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text='Да')
    builder.button(text='Нет')

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)
