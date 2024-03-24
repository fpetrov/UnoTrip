from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery, KeyboardButtonRequestUser, \
    KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from handlers.menu.states.trip_edit_state import TripEditState
from keyboards.row_keyboard import make_row_keyboard
from services.backend import BackendService

router = Router()

callback_answers = ['да', 'нет']


@router.callback_query(F.data.startswith('trip_add_companion_'))
async def trip_add_companion(callback: CallbackQuery,
                             state: FSMContext):
    reply = (f'👉 Хорошо, теперь выбери человека, которого хочешь добавить.\n'
             f'👉 Учти, что человек должен быть уже зарегистрирован в боте\n')

    trip_id = callback.data.split('_')[-1]

    await state.update_data(trip_id=trip_id)

    builder = ReplyKeyboardBuilder()

    builder.row(KeyboardButton(text='Выбрать пользователя',
                               request_user=KeyboardButtonRequestUser(request_id=0, user_is_bot=False)))

    await callback.message.answer(reply,
                                  reply_markup=builder.as_markup(resize_keyboard=True))

    await callback.answer()

    await state.set_state(TripEditState.waiting_for_friend)


async def get_full_name(bot: Bot, user_id):
    try:
        chat_member = await bot.get_chat_member(chat_id=user_id, user_id=user_id)
        full_name = chat_member.user.full_name

        return full_name
    except Exception as e:
        print(f"Error: {e}")
        return None


@router.message(TripEditState.waiting_for_friend)
async def friend_chosen(message: Message, state: FSMContext, backend: BackendService):
    current_data = await state.get_data()

    if message.user_shared:
        notification_list = await backend.trip_service.add_companion(current_data['trip_id'],
                                                                     message.user_shared.user_id)

        user_name = await get_full_name(message.bot, message.user_shared.user_id)
        for user in notification_list['subscribers']:
            await message.bot.send_message(user,
                                           text=f'🎉 {user_name} добавлен в путешествие!',
                                           reply_markup=ReplyKeyboardRemove())
    else:
        reply = f'Ты никого не выбрал :('
        await message.answer(reply)

    await state.set_state(None)
