from aiogram.filters import BaseFilter
from aiogram.types import Message


class AgeFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            age = int(message.text)
            return 8 <= age <= 100
        except ValueError:
            return False
