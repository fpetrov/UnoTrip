# from typing import Optional
# from aiogram.filters.callback_data import CallbackData
#
# import logging
#
# from aiogram import Bot, Dispatcher, types
# from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
# from aiogram import F
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
# from aiogram.filters.command import Command, CommandObject
#
# from contextlib import suppress
# from aiogram.exceptions import TelegramBadRequest
#
#
# class NumbersCallbackFactory(CallbackData, prefix='num'):
#     action: str
#     value: Optional[int]
#
#
# user_data = {}
#
#
# def get_keyboard_num() -> types.InlineKeyboardMarkup:
#     builder = InlineKeyboardBuilder()
#
#     builder.button(text='-2',
#                    callback_data=NumbersCallbackFactory(
#                        action='change', value=-2))
#
#     builder.button(text='-1',
#                    callback_data=NumbersCallbackFactory(
#                        action='change', value=-1))
#
#     builder.button(text='+1',
#                    callback_data=NumbersCallbackFactory(
#                        action='change', value=1))
#
#     builder.button(text='+2',
#                    callback_data=NumbersCallbackFactory(
#                        action='change', value=2))
#
#     builder.button(text='Подтвердить',
#                    callback_data=NumbersCallbackFactory(
#                        action='confirm'))
#
#     builder.adjust(4)
#
#     return builder.as_markup(resize_keyboard=True)
#
#
# async def update_text(message: types.Message, new_value: int):
#     with suppress(TelegramBadRequest):
#         await message.edit(f'Укажите число: {new_value}',
#                            reply_markup=get_keyboard_num())
#
#
# @dp.message(Command('numbers'))
# async def numbers_command(message: types.Message):
#     user_data[message.from_user.id] = 0
#
#     await message.answer('Укажите число: 0', reply_markup=get_keyboard_num())
#
#
# @dp.callback_query(NumbersCallbackFactory.filter(F.action == 'change'))
# async def callbacks_numbers_change(callback: types.CallbackQuery,
#                                    callback_data: NumbersCallbackFactory):
#
#     user_value = user_data.get(callback.from_user.id, 0)
#
#     user_data[callback.from_user.id] = user_value + callback_data.value
#
#     await update_text(callback.message, user_data[callback.from_user.id])
#     await callback.answer()
#
#
# @dp.callback_query(NumbersCallbackFactory.filter(F.action == 'confirm'))
# async def callbacks_numbers_confirm(callback: types.CallbackQuery,
#                                     callback_data: NumbersCallbackFactory):
#
#     user_value = user_data.get(callback.from_user.id, 0)
#
#     await callback.message.edit_text(f'Итого: {user_value}')
#     await callback.answer()
#
#
# @dp.callback_query(NumbersCallbackFactory.filter(F.action == 'confirm'))
# async def callbacks_numbers_confirm(callback_query: types.CallbackQuery, callback_data: NumbersCallbackFactory):
#     await update_text(callback_query.message, 0)
#     await callback_query.message.answer(f'Ваше число: {user_data[callback_query.from_user.id]}')