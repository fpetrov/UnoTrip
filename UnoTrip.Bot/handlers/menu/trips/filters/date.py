from datetime import datetime

from aiogram.filters import BaseFilter
from aiogram.types import Message

from typing import Union, Dict


class DateFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, datetime]]:
        try:
            date = datetime.strptime(message.text, '%Y-%m-%d').date()

            return {'date': date}
        except ValueError:
            return False
