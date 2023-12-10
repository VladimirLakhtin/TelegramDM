"""Receivers handlers file"""
import io

from aiogram.types import Message, CallbackQuery, Location
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from pyrogram.errors import UsernameInvalid

from src.bot.structures.funcs import standardization_receivers_data, get_receivers_from_chat
from src.bot.structures.states import MailingStatesGroup
from src.bot.structures.text import CaptureText as cpt_txt


async def input_receivers_file(message: Message, widget: MessageInput,
                               manager: DialogManager):
    if message.document.file_name.endswith('.txt'):
        file = await message.bot.get_file(message.document.file_id)
        with io.BytesIO() as file_in_io:
            await message.bot.download_file(file.file_path, file_in_io)
            data = file_in_io.read().decode("latin-1")
        manager.dialog_data['receivers'] = standardization_receivers_data(data)
        await manager.next()
    else:
        await manager.switch_to(MailingStatesGroup.rec_from_file)


async def confirm_receivers_file(callback: CallbackQuery, button: Button,
                                 manager: DialogManager):
    await callback.answer('Получатели установлены')
    await manager.switch_to(MailingStatesGroup.final_info)


async def input_receivers_chat(message: Message, widget: MessageInput,
                               manager: DialogManager):
    accounts = manager.start_data.get('accounts')
    chatname = message.text

    try:
        receivers = await get_receivers_from_chat(accounts[0].phone_number, chatname)
    except UsernameInvalid:
        await message.answer(cpt_txt.RECEIVERS_CHAT_ERROR)
        return

    if not receivers:
        await message.answer(cpt_txt.RECEIVERS_CHAT_NO_MEMBERS)
        return

    manager.dialog_data['receivers'] = receivers
    await manager.switch_to(MailingStatesGroup.final_info)


async def input_receivers_geo(location: Location, widget: MessageInput,
                              manager: DialogManager):
    print()



async def cancel_receivers(callback: CallbackQuery, button: Button,
                           manager: DialogManager):
    del manager.dialog_data['receivers']
    await manager.back()
