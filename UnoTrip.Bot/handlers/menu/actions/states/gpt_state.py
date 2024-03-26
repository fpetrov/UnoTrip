from aiogram.fsm.state import StatesGroup, State


class GptState(StatesGroup):
    waiting_for_prompt = State()
