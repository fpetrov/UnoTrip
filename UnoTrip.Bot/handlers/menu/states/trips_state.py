from aiogram.fsm.state import StatesGroup, State


class TripsState(StatesGroup):
    waiting_for_name = State()
    waiting_for_description = State()
