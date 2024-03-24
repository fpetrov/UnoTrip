from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery, InputFile, \
    BufferedInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.menu.states.trips_state import TripsState
from services.backend import BackendService
from services.open_street_map import OpenStreetMapService

router = Router()


@router.callback_query(F.data.startswith('trip_show_map_'))
async def trip_show_map_query(callback: CallbackQuery,
                              backend: BackendService,
                              open_street_map: OpenStreetMapService,
                              state: FSMContext):
    trip_id = callback.data.split('_')[-1]

    route = await backend.trip_service.get_route(trip_id)
    image_data = await open_street_map.take_screenshot(route)

    reply = f'ℹ️ Вот маршрут, по которому проходит путешествие'

    await callback.message.answer_photo(caption=reply,
                                        photo=BufferedInputFile(image_data, 'map.png'),
                                        parse_mode='HTML')

    await callback.answer()
