from aiogram import F, Router
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.content_type import ContentTypeFilter
from handlers.menu.states.trip_edit_state import TripEditState
from keyboards.row_keyboard import make_row_keyboard
from services.backend import BackendService
from services.open_street_map import OpenStreetMapService

router = Router()


@router.message(TripEditState.waiting_for_note_file,
                ContentTypeFilter([ContentType.VIDEO,
                                   ContentType.PHOTO,
                                   ContentType.DOCUMENT,
                                   ContentType.AUDIO,
                                   ContentType.VOICE,
                                   ContentType.VIDEO_NOTE]))
async def file_chosen(message: Message,
                      state: FSMContext,
                      backend: BackendService):
    if message.document:
        file_id = message.document.file_id
        content_type = ContentType.DOCUMENT
    elif message.photo:
        file_id = message.photo[-1].file_id
        content_type = ContentType.PHOTO
    elif message.video:
        file_id = message.video.file_id
        content_type = ContentType.VIDEO
    elif message.audio:
        file_id = message.audio.file_id
        content_type = ContentType.AUDIO
    elif message.voice:
        file_id = message.voice.file_id
        content_type = ContentType.VOICE
    elif message.video_note:
        file_id = message.video_note.file_id
        content_type = ContentType.VIDEO_NOTE

    await state.update_data(file_id=file_id)
    await state.update_data(content_type=content_type.value)

    print(content_type.value)

    current_data = await state.get_data()

    note_data = {
        'telegramId': message.from_user.id,
        'name': current_data['note_name'],
        'fileId': current_data['file_id'],
        'isPrivate': current_data['note_privacy'],
        'contentType': current_data['content_type']
    }

    await backend.trip_service.add_note(current_data['trip_id'],
                                        note_data)

    await message.answer(
        text=f'🎉 Отлично, заметка сохранена'
    )

    await state.set_state(None)


@router.message(TripEditState.waiting_for_note_file)
async def file_chosen_invalid(message: Message):
    await message.answer(
        text='❌ Похоже, что ты передал не поддерживающийся файл. Попробуй ещё раз'
    )
