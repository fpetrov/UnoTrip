import datetime

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.menu.states.trip_edit_state import TripEditState
from keyboards.row_keyboard import make_row_keyboard
from services.backend import BackendService
from services.open_street_map import OpenStreetMapService

router = Router()


@router.callback_query(F.data.startswith('top_3_facts_action_'))
async def trip_action_tab(callback: CallbackQuery,
                          state: FSMContext,
                          backend: BackendService):
    reply = f'👉 Хорошо, выбери нужную локацию. Учти, что запрос может занять некоторое время :)'

    trip_id = callback.data.split('_')[-1]
    trip_data = await backend.trip_service.get(trip_id)

    await state.update_data(trip_id=trip_id)

    builder = InlineKeyboardBuilder()

    for i, location in enumerate(trip_data['locations'], start=1):
        builder.row(InlineKeyboardButton(text=f"{i}. {location['name']}",
                                         callback_data=f'facts_question_{location["id"]}'))

    await callback.message.answer(
        text=reply,
        reply_markup=builder.as_markup()
    )

    await callback.answer()


@router.callback_query(F.data.startswith('facts_question_'))
async def location_facts_forecast(callback: CallbackQuery,
                                  state: FSMContext,
                                  backend: BackendService,
                                  open_street_map: OpenStreetMapService):
    location_id = callback.data.split('_')[-1]

    location = await backend.trip_service.get_location(location_id)

    response = await open_street_map.ask(f'Write top 3 interesting facts about {location["name"]}, you can write them shortly')

    await callback.message.answer(
        text=response,
        parse_mode='HTML'
    )

    await callback.answer()

