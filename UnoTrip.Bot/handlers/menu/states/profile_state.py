from aiogram.fsm.state import StatesGroup, State


class ProfileEditState(StatesGroup):
    waiting_for_age = State()
    waiting_for_city = State()
    waiting_for_bio = State()
