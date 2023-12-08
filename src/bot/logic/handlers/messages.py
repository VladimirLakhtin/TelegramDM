"""Messages handlers file"""
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
                          manager: DialogManager, item_id: str):
    manager.dialog_data['message_id'] = item_id
    await manager.switch_to(MessagesStatesGroup.details)


async def delete_message(callback: CallbackQuery, button: Button,
                         manager: DialogManager):
    db: Database = manager.middleware_data.get('db')
    message_id = manager.dialog_data.get('message_id')
    await db.message.delete(Message_db.id == message_id)
    await manager.switch_to(MessagesStatesGroup.lst)
