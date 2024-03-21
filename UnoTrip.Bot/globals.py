from aiogram import Bot, Dispatcher

from handlers import common
from handlers.registration import age_chosen, city_chosen

from filters.permission import PermissionFilter
from middlewares.chat_action import ChatActionMiddleware

from aiogram.fsm.storage.memory import MemoryStorage


async def run_app(token: str):
    bot = Bot(token)
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.middleware(ChatActionMiddleware())

    # TODO: Не забыть удалить этот фильтр
    dp.message.filter(PermissionFilter())

    dp.include_routers(common.router,
                       age_chosen.router,
                       city_chosen.router)

    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
