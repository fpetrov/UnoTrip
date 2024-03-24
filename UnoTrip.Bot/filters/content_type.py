from typing import Union

from aiogram.enums import ContentType
from aiogram.filters import BaseFilter
from aiogram.types import Message


class ContentTypeFilter(BaseFilter):
    def __init__(self, content_type: list[ContentType]):
        self.content_type = content_type

    async def __call__(self, message: Message) -> bool:
        return ContentType(message.content_type) in self.content_type
