from aiogram import Bot, Dispatcher

from handlers import (questions,
                      different_types,
                      group_games,
                      usernames,
                      common,
                      ordering_food)

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
                       ordering_food.router,
                       questions.router,
                       usernames.router,
                       group_games.router,
                       different_types.router)

    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
