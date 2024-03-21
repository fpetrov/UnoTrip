from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.for_questions import get_keyboard

router = Router()

@router.message(Command('start'))
async def start_command(message: Message):
    await message.answer('Вы довольны своей работой',
                         reply_markup=get_keyboard())


@router.message(F.text.lower() == 'да')
async def yes_answer(message: Message):
    await message.answer('Круто!',
                         reply_markup=ReplyKeyboardRemove())


@router.message(F.text.lower() == 'нет')
async def no_answer(message: Message):
    await message.answer('Ну и ладно',
                         reply_markup=ReplyKeyboardRemove())
