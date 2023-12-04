from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from src.bot.structures.states import MessagesStatesGroup
from src.db import Database, Message as Message_db


async def input_message_text(message: Message, widget: MessageInput,
                             manager: DialogManager):
    manager.dialog_data['title'] = message.text
    await manager.next()


async def confirm_create_message(message: Message, widget: MessageInput,
                                 manager: DialogManager):
    manager.dialog_data['message'] = message.text
    await manager.next()


async def create_message(callback: CallbackQuery, button: Button,
                         manager: DialogManager):
    title = manager.dialog_data["title"]
    text = manager.dialog_data["message"]
    db: Database = manager.middleware_data.get('db')
    await db.message.new(title=title, text=text)
    await manager.switch_to(MessagesStatesGroup.lst)


async def message_details(callback: CallbackQuery, button: Button,
                          manager: DialogManager, button_text: str):
    db: Database = manager.middleware_data.get('db')
    message = await db.message.get_by_where(Message_db.title == button_text)
    if message is None:
        return
    manager.dialog_data['message_id'] = message.id
    await manager.switch_to(MessagesStatesGroup.details)


async def delete_message(callback: CallbackQuery, button: Button,
                         manager: DialogManager):
    db: Database = manager.middleware_data.get('db')
    message_id = manager.dialog_data.get('message_id')
    await db.message.delete(Message_db.id == message_id)
    await manager.switch_to(MessagesStatesGroup.lst)
