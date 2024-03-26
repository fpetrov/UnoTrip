import datetime

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.menu.actions.common.show_variants import show_variants
from handlers.menu.states.trip_edit_state import TripEditState
from keyboards.row_keyboard import make_row_keyboard
from services.backend import BackendService
from services.open_street_map import OpenStreetMapService

router = Router()


@router.callback_query(F.data.startswith('wiki_action_'))
async def wiki_action_tab(callback: CallbackQuery,
                          state: FSMContext,
                          backend: BackendService):
    reply = f'👉 Хорошо, выбери нужную локацию'

    trip_id = callback.data.split('_')[-1]
    trip_data = await backend.trip_service.get(trip_id)

    await state.update_data(trip_id=trip_id)

    builder = InlineKeyboardBuilder()

    for i, location in enumerate(trip_data['locations'], start=1):
        builder.row(InlineKeyboardButton(text=f"{i}. {location['name']}",
                                         callback_data=f'wiki_show_{location["id"]}'))

    await callback.message.answer(
        text=reply,
        reply_markup=builder.as_markup()
    )

    await callback.answer()


@router.callback_query(F.data.startswith('wiki_show_'))
async def show_wiki(callback: CallbackQuery,
                    state: FSMContext,
                    backend: BackendService):
    location_id = callback.data.split('_')[-1]

    location = await backend.trip_service.get_location(location_id)
    summary, url = backend.places_service.get_wiki_article(location['name'])

    if not summary:
        summary = '🤷‍♂️ Ничего не нашел ️'
        await callback.message.answer(summary)
        await callback.answer()
        return

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='🔗 Открыть в браузере', web_app=WebAppInfo(url=url)))

    await callback.message.answer(summary,
                                  reply_markup=builder.as_markup())

    await callback.answer()
