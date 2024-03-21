import asyncio
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message

from aiogram.dispatcher.flags import get_flag
from aiogram.utils.chat_action import ChatActionSender


class ChatActionMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        long_operation_type = get_flag(data, 'long_operation')

        if not long_operation_type:
            return await handler(event, data)

        async with ChatActionSender(
            action=long_operation_type,
            bot=event.bot,
            chat_id=event.chat.id
        ):
            return await handler(event, data)
