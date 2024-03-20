import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.filters.command import Command

logging.basicConfig(level=logging.INFO)
bot = Bot(token="7127938588:AAGkdGD0GIkblUPrnoDO1oVZ6ttIQ-sOfjY")
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    template = [
        [types.KeyboardButton(text='Open map',
                              web_app=WebAppInfo(url='https://graphhopper.com/maps/?point=55.731876%2C37.607434_55.731876%2C+37.607434&point=55.73639%2C37.593595_55.736390%2C+37.593595&point=48.853495%2C2.348392_Paris%2C+%C3%8Ele-de-France%2C+France&profile=car&layer=Omniscale'))],
        [types.KeyboardButton(text="Skip")]
    ]

    markup = types.ReplyKeyboardMarkup(keyboard=template)

    await message.answer("Hello!", reply_markup=markup)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


# TODO: Сделать Filter Middleware, чтобы доступ был только мне