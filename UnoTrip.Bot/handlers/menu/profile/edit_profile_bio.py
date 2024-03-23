from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.menu.states.profile_state import ProfileEditState
from services.backend import BackendService

router = Router()


@router.callback_query(F.data == 'profile_edit_bio')
async def profile_edit_age(callback: CallbackQuery,
                           state: FSMContext):
    reply = f'Хорошо, теперь свое новое описание (от 1 до 150 символов)\n'

    await callback.message.answer(reply)

    await callback.answer()

    await state.set_state(ProfileEditState.waiting_for_bio)


@router.message(ProfileEditState.waiting_for_bio,
                F.text.len() >= 1,
                F.text.len() <= 150)
async def bio_chosen(message: Message,
                     state: FSMContext,
                     backend: BackendService):
    await state.update_data(bio=message.text)

    current_data = await state.get_data()

    await backend.user_service.update(
        message.from_user.id,
        {
            'description': current_data['bio']
        })

    await state.set_state(None)

    await message.answer(
        text='Отлично, ты изменил описание профиля',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(ProfileEditState.waiting_for_bio)
async def bio_chosen_invalid(message: Message):
    await message.answer(
        text='Похоже, что ты ввел описание в неверном формате. Попробуй ещё раз'
    )
