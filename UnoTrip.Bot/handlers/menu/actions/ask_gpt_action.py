import datetime

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.menu.actions.states.gpt_state import GptState
from handlers.menu.states.trip_edit_state import TripEditState
from keyboards.row_keyboard import make_row_keyboard
from services.backend import BackendService
from services.open_street_map import OpenStreetMapService

router = Router()


@router.callback_query(F.text == 'ask_gpt_action')
async def trip_action_tab(callback: CallbackQuery,
                          state: FSMContext,
                          backend: BackendService):
    reply = f'👉 Теперь задай свой вопрос боту (лучше всего задавать на английском языке, так как LLM лучше всего понимает именно его). Учти, что запрос может занять некоторое время :)'

    await callback.message.answer(
        text=reply
    )

    await state.set_state(GptState.waiting_for_prompt)

    await callback.answer()


@router.message(F.text, StateFilter(GptState.waiting_for_prompt),
                flags={"long_operation": "typing"})
async def prompt_answer(message: Message,
                        state: FSMContext,
                        backend: BackendService,
                        open_street_map: OpenStreetMapService):
    response = await open_street_map.ask(message.text)

    await message.answer(
        text=response,
        parse_mode='HTML'
    )

    await state.set_state(None)
