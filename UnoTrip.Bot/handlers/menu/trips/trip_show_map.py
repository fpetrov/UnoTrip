from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery, InputFile, \
    BufferedInputFile, FSInputFile
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
    user_id = callback.from_user.id

    route = await backend.trip_service.get_route(user_id, trip_id)

    if len(route['destinations']) < 2:
        await callback.message.answer('❌ Слишком мало точек для показа маршрута, необходимо хотя бы 2 локации',
                                      reply_markup=ReplyKeyboardRemove())
        await callback.answer()

        return

    image = await open_street_map.take_screenshot(route)

    reply = f'ℹ️ Вот маршрут, по которому проходит путешествие'

    await callback.message.answer_photo(caption=reply,
                                        photo=BufferedInputFile(file=image, filename='map.png'),
                                        parse_mode='HTML')

    await callback.answer()
