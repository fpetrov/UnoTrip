from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message


class PermissionFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in [1884964253, 5888875072]
