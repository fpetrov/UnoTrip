import datetime
import time

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

callback_answers = ['да', 'нет']


@router.callback_query(F.data.startswith('weather_action_'))
async def trip_action_tab(callback: CallbackQuery,
                          state: FSMContext,
                          backend: BackendService):
    reply = f'👉 Хорошо, выбери нужную локацию'

    trip_id = callback.data.split('_')[-1]
    trip_data = await backend.trip_service.get(trip_id)

    await state.update_data(trip_id=trip_id)

    builder = InlineKeyboardBuilder()

    for i, location in enumerate(trip_data['locations'], start=1):
        builder.row(InlineKeyboardButton(text=f"{i}. {location['name']}",
                                         callback_data=f'weather_forecast_{location["id"]}'))

    await callback.message.answer(
        text=reply,
        reply_markup=builder.as_markup()
    )

    await callback.answer()


@router.callback_query(F.data.startswith('weather_forecast_'))
async def location_weather_forecast(callback: CallbackQuery,
                                    state: FSMContext,
                                    backend: BackendService,
                                    open_street_map: OpenStreetMapService):
    location_id = callback.data.split('_')[-1]
    location = await backend.trip_service.get_location(location_id)

    utc_now = datetime.datetime.now(datetime.UTC)
    start_date = datetime.datetime.strptime(location['start'], '%Y-%m-%d').date()

    if start_date > utc_now:
        result = utc_now
    else:
        result = start_date

    forecast = await open_street_map.get_forecast(result.strftime('%Y-%m-%d'),
                                                  location['name'],
                                                  location['lat'],
                                                  location['lng'])

    if forecast is None:
        forecast = await open_street_map.get_forecast(utc_now.strftime('%Y-%m-%d'),
                                                  location['name'],
                                                  location['lat'],
                                                  location['lng'])

    weather = f'🌡️ Прогноз погоды в {location["name"]}:\n\n'

    current_weather = forecast['current_weather']
    weather += '<b>Сегодня</b>\n'
    weather += f'📅 {datetime.date.today()}\n'
    weather += f'🌡️ <b>Температура:</b> {current_weather["temperature"]}°C\n'
    weather += f'🌡️ <b>Ощущается как</b> {current_weather["apparent_temperature"]}°C\n\n\n'

    for i, day in enumerate(forecast['weather_forecast'], start=1):
        weather += f'📅 <b>{day["date"]}</b>\n'
        weather += f'☀️ <b>Утром:</b> {day["morning"]}°C,     {parse_weather_type(day["weather_type"][0])} \n'
        weather += '---------------\n'
        weather += f'🌅 <b>Днем:</b> {day["day"]}°C,     {parse_weather_type(day["weather_type"][1])} \n'
        weather += '---------------\n'
        weather += f'🌇 <b>Вечером:</b> {day["evening"]}°C,     {parse_weather_type(day["weather_type"][2])} \n'
        weather += '---------------\n'
        weather += f'🌃 <b>Ночью:</b> {day["night"]}°C,     {parse_weather_type(day["weather_type"][3])} \n\n\n'

    await callback.message.answer(
        text=weather,
        parse_mode='HTML'
    )

    await callback.answer()

    await state.set_state(None)


def parse_weather_type(weather_type: int):
    weather_text = get_weather_text(weather_type)

    if weather_text == 'Ясное небо':
        return '☀️ ' + weather_text
    elif weather_text in ['Преимущественно ясно', 'Переменная облачность']:
        return '⛅️ ' + weather_text
    elif weather_text in ['Пасмурно', 'Туман и инеющий туман']:
        return '☁️ ' + weather_text
    elif weather_text.startswith('Морось'):
        return '🌦️ ' + weather_text
    elif weather_text.startswith('Дождь'):
        return '🌧️ ' + weather_text
    elif weather_text.startswith('Гроза'):
        return '⛈️ ' + weather_text
    elif weather_text.startswith('Снег'):
        return '❄️ ' + weather_text
    elif weather_text in ['Туман', 'Снежные зерна']:
        return '🌫️ ' + weather_text
    elif weather_text == 'Снегопад с прояснениями: сильная интенсивность':
        return '🌪️ ' + weather_text
    else:
        return '☀️ ' + weather_text


def get_weather_text(weather_code: int):
    weather_mapping = {
        0: 'Ясное небо',
        1: 'Преимущественно ясно',
        2: 'Переменная облачность',
        3: 'Пасмурно',
        45: 'Туман',
        48: 'Туман и инеем',
        51: 'Легкая морось',
        53: 'Средняя морось',
        55: 'Сильная морось',
        56: 'Легкая изморозь',
        57: 'Сильная изморозь',
        61: 'Небольшой дождь: небольшая интенсивность',
        63: 'Средняя дождливость',
        65: 'Сильная дождливость',
        66: 'Легкий ледяной дождь',
        67: 'Сильный ледяной дождь',
        71: 'Снег: небольшая интенсивность',
        73: 'Снег: умеренная интенсивность',
        75: 'Снег: сильная интенсивность',
        77: 'Град',
        80: 'Дождь с прояснениями: небольшая интенсивность',
        81: 'Дождь с прояснениями: умеренная интенсивность',
        82: 'Дождь с прояснениями: сильная интенсивность',
        85: 'Снегопад с прояснениями: небольшая интенсивность',
        86: 'Снегопад с прояснениями: сильная интенсивность',
        95: 'Гроза: небольшая или умеренная интенсивность',
        96: 'Гроза с градом: небольшая интенсивность',
        99: 'Гроза с градом: сильная интенсивность'
    }

    return weather_mapping.get(weather_code, 'Неизвестно')

