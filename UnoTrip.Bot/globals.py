from aiogram import Bot, Dispatcher

from handlers import common
from handlers.registration import age_chosen, city_chosen, bio_chosen

from filters.permission import PermissionFilter
from middlewares.chat_action import ChatActionMiddleware

from aiogram.fsm.storage.memory import MemoryStorage

from services.backend import BackendService
from services.open_street_map import OpenStreetMapService


async def run_app(token: str):
    bot = Bot(token)
    dp = Dispatcher(storage=MemoryStorage(),
                    backend=BackendService('http://localhost:5174/api'),
                    open_street_map=OpenStreetMapService('http://localhost:8000'))

    dp.message.middleware(ChatActionMiddleware())

    # TODO: Не забыть удалить этот фильтр
    dp.message.filter(PermissionFilter())

    # Общие обработчики
    dp.include_router(common.router)

    # Регистрация пользователя
    dp.include_routers(age_chosen.router,
                       city_chosen.router,
                       bio_chosen.router)

    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
