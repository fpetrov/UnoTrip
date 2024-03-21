from aiogram import Router
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import Message
from aiogram.filters import Command

from filters.chat_type import ChatTypeFilter

router = Router()

# Фильтры можно прикреплять прямо к роутерам
router.message.filter(
    ChatTypeFilter(chat_type=['group', 'supergroup'])
)


@router.message(Command('dice'))
async def dice_command(message: Message):
    await message.answer_dice(emoji=DiceEmoji.DART)


@router.message(Command('basketball'))
async def basketball_command(message: Message):
    await message.answer_dice(emoji=DiceEmoji.BASKETBALL)
