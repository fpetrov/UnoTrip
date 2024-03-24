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

router = Router()

callback_answers = ['да', 'нет']


@router.callback_query(F.data.startswith('trip_delete_location_'))
async def trip_delete_location(callback: CallbackQuery,
                               state: FSMContext,
                               backend: BackendService):
    reply = f'Хорошо, теперь выбери локацию, которую хочешь удалить'

    trip_id = callback.data.split('_')[-1]
    trip_data = await backend.trip_service.get(trip_id)

    await state.update_data(trip_id=trip_id)

    builder = InlineKeyboardBuilder()

    for i, location in enumerate(trip_data['locations'], start=1):
        builder.row(InlineKeyboardButton(text=f"{i}. {location['name']}",
                                         callback_data=f'trip_remove_location_with_{location["id"]}'))

    await callback.message.answer(
        text=reply,
        reply_markup=builder.as_markup()
    )

    await callback.answer()


@router.callback_query(F.data.startswith('trip_remove_location_with_'))
async def trip_remove_location_with(callback: CallbackQuery,
                                    state: FSMContext,
                                    backend: BackendService):
    location_id = callback.data.split('_')[-1]

    current_data = await state.get_data()

    await backend.trip_service.delete_location(
        current_data['trip_id'], location_id)

    await callback.message.answer(
        text='🎉 Отлично, локация удалена'
    )

    await callback.answer()

    await state.set_state(None)
