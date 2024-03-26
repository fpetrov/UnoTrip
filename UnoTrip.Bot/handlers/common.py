from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove

from handlers.registration.states.registration import RegistrationState

router = Router()


@router.message(Command('start'))
async def start_command(message: Message,
                        state: FSMContext):
    current_data = await state.get_data()

    if current_data.get('registered', False):
        await message.answer(text='Ты уже зарегистрирован. Чтобы перейти в меню, нажми /menu',)
        return

    await message.answer(text='Привет! 👋 Это бот для удобного планирования твоих путешествий. 🏖\n'
                              'Давай сначала заполним твой профиль. Сколько тебе лет?',
                         reply_markup=ReplyKeyboardRemove())

    await state.set_state(RegistrationState.waiting_for_age)


@router.message(StateFilter(None), Command('cancel'))
@router.message(default_state, F.text.lower() == 'отмена')
async def cancel_command_no_state(message: Message,
                                  state: FSMContext):
    await state.set_data({})

    await message.answer(text='Действие отменено',
                         reply_markup=ReplyKeyboardRemove())


@router.message(Command('cancel'))
@router.message(F.text.lower() == 'отмена')
async def cancel_command(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        text='Действие отменено',
        reply_markup=ReplyKeyboardRemove())


# @router.message(StateFilter(None))
# async def cancel_callback(callback: CallbackQuery,
#                           state: FSMContext):
#     return
