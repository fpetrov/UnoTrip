from aiogram import Bot, Dispatcher
from redis.asyncio import Redis
from aiogram.methods import DeleteWebhook

from handlers import common
from handlers import menu_tab

from handlers.menu.profile import profile_tab
from handlers.registration import age_chosen, city_chosen, bio_chosen
from handlers.menu.profile import edit_profile_age, edit_profile_city, edit_profile_bio

from handlers.menu.trips import (trips_tab, trips_all, trips_view, trips_create, trip_add_companion,
                                 trip_add_location_start, trip_add_location_end, trip_add_location_name,
                                 trip_delete_location, trip_edit_description, trip_edit_name, trip_add_note_name,
                                 trip_add_note_file, trip_notes_all, trip_add_note_mode, trip_notes_tab,
                                 trip_show_map, trip_actions_tab)

from handlers.menu.actions import (top_3_facts_action, weather_action, ask_gpt_action, attractions_action, cafe_action,
                                   car_rent_action, hotel_action, bar_action, pharmacy_action, wiki_action)

from filters.permission import PermissionFilter
from middlewares.chat_action import ChatActionMiddleware

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from services.backend import BackendService
from services.open_street_map import OpenStreetMapService

import os


async def run_app(token: str):
    bot = Bot(token)

    redis_host = os.environ.get("REDIS_HOST", "localhost")
    redis_port = int(os.environ.get("REDIS_PORT", "6379"))

    # api_host = os.environ.get("API_HOST")

    api_host = 'http://localhost:5174'

    #storage = RedisStorage(Redis(host=redis_host, port=redis_port, db=0))

    storage = MemoryStorage()

    #fsq3Y8z+w9u3UaJn02eTjzHv08mYxp59vYlkY//DhHGB7vE=

    dp = Dispatcher(storage=storage,
                    backend=BackendService(f'{api_host}/api', places_token='fsq3Y8z+w9u3UaJn02eTjzHv08mYxp59vYlkY//DhHGB7vE='),
                    open_street_map=OpenStreetMapService('http://176.53.161.198:8000'))

    dp.message.middleware(ChatActionMiddleware())

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
                       trip_add_note_name.router,
                       trip_show_map.router,
                       trip_actions_tab.router)

    dp.include_routers(top_3_facts_action.router,
                       weather_action.router,
                       ask_gpt_action.router,
                       attractions_action.router,
                       cafe_action.router,
                       hotel_action.router,
                       car_rent_action.router,
                       pharmacy_action.router,
                       bar_action.router,
                       wiki_action.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
