from aiogram import F, Router
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery, InputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.backend import BackendService

router = Router()


@router.callback_query(F.data == 'trip_notes_all')
async def notes_command(callback: CallbackQuery,
                        state: FSMContext,
                        backend: BackendService):
    current_data = await state.get_data()

    notes = await backend.trip_service.get_my_notes(
        callback.from_user.id,
        current_data['trip_id'])
    builder = InlineKeyboardBuilder()

    for i, note in enumerate(notes, start=1):
        builder.row(InlineKeyboardButton(text=f"{i}. {note['name']}",
                                         callback_data=f'trip_nigger_note_{note["id"]}'))

    builder.adjust(5)

    builder.row(InlineKeyboardButton(text='🔙 Назад',
                                     callback_data='trip_view_' + current_data['trip_id']))

    reply = f'👉 Выбери, заметку, которую хочешь получить'

    await callback.message.answer(reply,
                                  reply_markup=builder.as_markup())

    await callback.answer()


@router.callback_query(F.data.startswith('trip_nigger_note_'))
async def view_note_command(callback: CallbackQuery,
                            state: FSMContext,
                            backend: BackendService):
    current_data = await state.get_data()

    note_id = callback.data.split('_')[-1]

    note_data = {}

    notes = await backend.trip_service.get_my_notes(
        callback.from_user.id,
        current_data['trip_id'])

    for note in notes:
        if note['id'] == int(note_id):
            note_data = note
            break

    await match_file_type(callback,
                          note_data['contentType'],
                          note_data['fileId'])

    await callback.answer()


async def match_file_type(callback: CallbackQuery,
                          content_type: ContentType,
                          file_id):
    if content_type == ContentType.DOCUMENT:
        await callback.message.answer_document(file_id)

    elif content_type == ContentType.VIDEO:
        await callback.message.answer_video(file_id)

    elif content_type == ContentType.AUDIO:
        await callback.message.answer_audio(file_id)

    elif content_type == ContentType.PHOTO:
        await callback.message.answer_photo(file_id)

    elif content_type == ContentType.VOICE:
        await callback.message.answer_voice(file_id)

    elif content_type == ContentType.VIDEO_NOTE:
        await callback.message.answer_video_note(file_id)
