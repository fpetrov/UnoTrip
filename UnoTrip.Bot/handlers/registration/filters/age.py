from aiogram.filters import BaseFilter
from aiogram.types import Message

from typing import Union, Dict


class AgeFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, int]]:
        try:
            age = int(message.text)

            if 8 <= age <= 100:
                return {'age': age}

            return False
        except ValueError:
            return False
