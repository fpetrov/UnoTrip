from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_row_keyboard(*buttons: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=button.capitalize()) for button in buttons],
        ],
        resize_keyboard=True
    )
