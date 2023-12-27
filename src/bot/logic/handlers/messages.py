"""Messages handlers file"""
from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from src.bot.structures.funcs import get_slug
from src.bot.structures.states import MessagesStatesGroup
from src.db import Database, Message as Message_db
from src.config import conf
from src.bot.structures.text import CaptureText as cpt_txt


async def input_message_title(message: Message, widget: MessageInput,
                              manager: DialogManager):
    db: Database = manager.middleware_data.get('db')
    title = message.text
    exists = await db.message.get_by_where(Message_db.title == title)
    if exists:
        await message.answer(cpt_txt.MESSAGE_TITLE_INPUT_UNIQUE)
        return

    manager.dialog_data['title'] = message.text
    await manager.next()


async def input_message_text(message: Message, widget: MessageInput,
                             manager: DialogManager):
    manager.dialog_data['message'] = message.text
    await manager.next()


async def input_message_media(message: Message, widget: MessageInput,
                              manager: DialogManager):
    if message.photo:
        manager.dialog_data['media'] = (
            message.photo[-1].file_id,
            message.photo[-1].file_unique_id,
            ContentType.PHOTO,
        )
    elif message.video:
        manager.dialog_data['media'] = (
            message.video.file_id,
            message.video.file_unique_id,
            ContentType.VIDEO,
        )
    await manager.next()


async def back_from_media_input(message: Message, widget: MessageInput,
                                manager: DialogManager):
    if manager.dialog_data.get('media'):
        del manager.dialog_data['media']


async def confirm_create_message(callback: CallbackQuery, button: Button,
                                 manager: DialogManager):
    db: Database = manager.middleware_data.get('db')
    title = manager.dialog_data.get("title")
    text = manager.dialog_data.get("message")
    file_id, _, content_type = manager.dialog_data.get(
        "media", (None, None, ContentType.TEXT))

    media_path = None
    if file_id:
        media = await callback.bot.get_file(file_id)
        extension = "jpeg" if content_type == ContentType.PHOTO else "mp4"
        filename = f'{title}_{get_slug()}.{extension}'
        media_path = conf.media_dir / filename
        await callback.bot.download_file(media.file_path, media_path)

    await db.message.new(
        title=title,
        text=text,
        content_type=content_type,
        media_path=media_path and str(media_path),
    )

    if 'media' in manager.dialog_data:
        del manager.dialog_data['media']
    await manager.switch_to(MessagesStatesGroup.lst)


async def message_details(callback: CallbackQuery, button: Button,
                          manager: DialogManager, item_id: str):
    manager.dialog_data['message_id'] = item_id
    await manager.switch_to(MessagesStatesGroup.details)


async def delete_message(callback: CallbackQuery, button: Button,
                         manager: DialogManager):
    db: Database = manager.middleware_data.get('db')
    message_id = manager.dialog_data.get('message_id')
    await db.message.delete(message_id)
    await manager.switch_to(MessagesStatesGroup.lst)
