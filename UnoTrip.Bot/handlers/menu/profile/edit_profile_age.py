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


@router.callback_query(F.data == 'profile_edit_age')
async def profile_edit_age(callback: CallbackQuery,
                           state: FSMContext):
    reply = f'✒️ Хорошо, теперь введи свой новый возраст\n'

    await callback.message.answer(reply)

    await callback.answer()

    await state.set_state(ProfileEditState.waiting_for_age)


@router.message(ProfileEditState.waiting_for_age,
                AgeFilter())
async def age_chosen(message: Message,
                     state: FSMContext,
                     backend: BackendService,
                     age: int):

    await state.update_data(age=age)

    current_data = await state.get_data()

    await backend.user_service.update(
        message.from_user.id,
        {
            'age': current_data['age']
        })

    await state.set_state(None)

    await message.answer(
        text='🎉 Отлично, ты изменил свой возраст',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(ProfileEditState.waiting_for_age)
async def age_chosen_invalid(message: Message):
    await message.answer(
        text='❌ Похоже, что ты ввел возраст в неверном формате. Попробуй ещё раз',
        reply_markup=ReplyKeyboardRemove()
    )
