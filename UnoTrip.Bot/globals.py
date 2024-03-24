from aiogram import Bot, Dispatcher
from redis.asyncio import Redis

from handlers import common
from handlers import menu_tab

from handlers.menu.profile import profile_tab
from handlers.registration import age_chosen, city_chosen, bio_chosen
from handlers.menu.profile import edit_profile_age, edit_profile_city, edit_profile_bio

from handlers.menu.trips import trips_tab, trips_all, trips_view, trips_create, trip_add_companion, trip_add_location_start, trip_add_location_end, trip_add_location_name, trip_delete_location, trip_edit_description, trip_edit_name, trip_add_note_name, trip_add_note_file, trip_notes_all, trip_add_note_mode, trip_notes_tab

from filters.permission import PermissionFilter
from middlewares.chat_action import ChatActionMiddleware

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from services.backend import BackendService
from services.open_street_map import OpenStreetMapService


async def run_app(token: str):
    bot = Bot(token)

    # storage = RedisStorage(Redis(host='127.0.0.1', port=6379, db=0))

    storage = MemoryStorage()

    dp = Dispatcher(storage=storage,
                    backend=BackendService('http://localhost:5174/api'),
                    open_street_map=OpenStreetMapService('http://176.53.161.198:8000'))

    dp.message.middleware(ChatActionMiddleware())

    # TODO: Не забыть удалить этот фильтр
    dp.message.filter(PermissionFilter())

    # Общие обработчики
    dp.include_router(common.router)

    # Регистрация пользователя
    dp.include_routers(age_chosen.router,
                       city_chosen.router,
                       bio_chosen.router)

    # Меню
    dp.include_routers(menu_tab.router,
                       profile_tab.router,
                       edit_profile_age.router,
                       edit_profile_city.router,
                       edit_profile_bio.router)

    # Путешествия
    dp.include_routers(trips_tab.router,
                       trips_all.router,
                       trips_view.router,
                       trips_create.router,
                       trip_add_companion.router,
                       trip_add_location_start.router,
                       trip_add_location_end.router,
                       trip_delete_location.router,
                       trip_edit_description.router,
                       trip_edit_name.router,
                       trip_add_location_name.router,
                       trip_notes_tab.router,
                       trip_add_note_mode.router,
                       trip_notes_all.router,
                       trip_add_note_file.router,
                       trip_add_note_name.router)

    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
