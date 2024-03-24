from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.menu.states.trips_state import TripsState
from services.backend import BackendService

router = Router()


@router.callback_query(F.data == 'trips_create')
async def trips_create_query(callback: CallbackQuery,
                             backend: BackendService,
                             state: FSMContext):
    reply = f'Чтобы создать путешествие, введи его название\n'

    await state.set_state(TripsState.waiting_for_name)
    await callback.message.answer(reply)

    await callback.answer()


@router.message(TripsState.waiting_for_name,
                F.text.len() >= 1,
                F.text.len() <= 150)
async def trips_name_chosen(message: Message,
                            state: FSMContext):
    await state.update_data(trip_name=message.text)

    reply = f'Отлично, теперь введи описание путешествия\n'

    await state.set_state(TripsState.waiting_for_description)
    await message.answer(reply)


@router.message(TripsState.waiting_for_name)
async def name_chosen_invalid(message: Message):
    await message.answer(
        text='❌ Похоже, что ты ввел название в неверном формате. Попробуй ещё раз'
    )


@router.message(TripsState.waiting_for_description,
                F.text.len() >= 1,
                F.text.len() <= 150)
async def trips_description_chosen(message: Message,
                                   state: FSMContext,
                                   backend: BackendService):
    await state.update_data(trip_description=message.text)

    current_data = await state.get_data()

    result = await backend.trip_service.create(message.from_user.id,
                                               current_data['trip_name'],
                                               current_data['trip_description'])

    if not result:
        await message.answer(
            text='❌ Похоже, что ты ввел название, которое уже существует в твоих путешествиях. Попробуй ещё раз'
        )
        return

    await state.set_state(None)

    await message.answer('🎉 Путешествие создано')

    await message.answer(
        text='Хочешь создать добавить маршрут в путешествие?',
        reply_markup=InlineKeyboardBuilder()
        .row(InlineKeyboardButton(text='✅ Да',
                                  callback_data=f'trip_add_location_{result["uuid"]}'))
        .row(InlineKeyboardButton(text='🔙 Нет',
                                  callback_data='menu_trips'))
        .as_markup()
    )


@router.message(TripsState.waiting_for_description)
async def description_chosen_invalid(message: Message):
    await message.answer(
        text='❌ Похоже, что ты ввел описание в неверном формате. Попробуй ещё раз'
    )
