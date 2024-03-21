from typing import List

from aiogram import Router, F
from aiogram.types import Message

from filters.find_usernames import HasUsernamesFilter
from middlewares.slowpoke import SlowpokeMiddleware

router = Router()

router.message.middleware(SlowpokeMiddleware(2))


@router.message(F.text,
                HasUsernamesFilter(),
                flags={'long_operation': 'typing'})
async def message_with_text(message: Message,
                            usernames: List[str]):
    await message.reply(
        f'Спасибо! Обязательно подпишусь на '
        f'{", ".join(usernames)}'
    )
