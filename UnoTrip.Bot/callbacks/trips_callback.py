from typing import Optional
from aiogram.filters.callback_data import CallbackData


class TripsViewCallback(CallbackData, prefix="trip"):
    id: int
