from aiogram.fsm.state import StatesGroup, State


class TripEditState(StatesGroup):
    waiting_for_name = State()
    waiting_for_description = State()

    waiting_for_location_name = State()
    waiting_for_location_start = State()
    waiting_for_location_end = State()

    waiting_for_friend = State()

    waiting_for_note_privacy = State()
    waiting_for_note_name = State()
    waiting_for_note_file = State()
