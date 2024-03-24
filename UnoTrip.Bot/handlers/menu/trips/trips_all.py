from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.registration.filters.age import AgeFilter
from handlers.menu.states.profile_state import ProfileEditState
from services.backend import BackendService

router = Router()


@router.callback_query(F.data == 'trips_all')
async def trips_all_query(callback: CallbackQuery,
                          backend: BackendService):
    reply = (f'🏖 Вот список всех твоих путешествий.\n'
             f'Учти, что одновременно отображаться могут лишь 7 путешествий (если их больше, то они будут скрыты)')

    my_trips = await backend.trip_service.get_my(callback.from_user.id)

    print(my_trips)

    builder = InlineKeyboardBuilder()

    for i, trip in enumerate(my_trips[:7], start=1):
        builder.row(InlineKeyboardButton(text=f"{i}. {trip['name']}",
                                         callback_data=f"trip_view_{trip['uuid']}"))

    builder.row(InlineKeyboardButton(text='🔙 Назад',
                                     callback_data='menu_trips'))

    await callback.message.answer(reply,
                                  reply_markup=builder.as_markup())

    await callback.answer()
