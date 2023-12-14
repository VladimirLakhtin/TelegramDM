"""Receivers handlers file"""
import io

from aiogram.types import Message, CallbackQuery, Location
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from pyrogram.errors import UsernameInvalid, UsernameNotOccupied

from src.bot.structures.funcs import standardization_receivers_data, get_receivers_from_users, \
    get_receivers_from_members, clear_accounts_on_auth
from src.bot.structures.pyrogram_funcs import get_chat_members, get_users_nearly
from src.bot.structures.states import MailingStatesGroup
from src.bot.structures.text import CaptureText as cpt_txt
from src.db import Database, Account


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
    db: Database = manager.middleware_data.get('db')
    accounts = manager.start_data.get('accounts')
    chatname = message.text

    no_auth_accounts = await clear_accounts_on_auth(accounts)
    for acc in no_auth_accounts:
        manager.start_data['accounts'].remove(acc)
        await db.account.delete(acc.id)

    if not accounts:
        await message.answer(cpt_txt.MAILING_NO_ACCOUNTS)
        await manager.done()
        return

    try:
        members = await get_chat_members(accounts[0].phone_number, chatname)
    except (UsernameInvalid, UsernameNotOccupied):
        await message.answer(cpt_txt.RECEIVERS_CHAT_ERROR)
        return

    receivers = get_receivers_from_members(members)

    if not receivers:
        await message.answer(cpt_txt.RECEIVERS_CHAT_NO_MEMBERS)
        return

    manager.dialog_data['receivers'] = receivers
    await manager.switch_to(MailingStatesGroup.final_info)


async def input_receivers_geo(message: Message, widget: MessageInput,
                              manager: DialogManager):
    db: Database = manager.middleware_data.get('db')
    location = message.location
    accounts = manager.start_data.get('accounts')

    no_auth_accounts = await clear_accounts_on_auth(accounts)
    for acc in no_auth_accounts:
        manager.start_data['accounts'].remove(acc)
        await db.account.delete(acc.id)

    if not accounts:
        await message.answer(cpt_txt.MAILING_NO_ACCOUNTS)
        await manager.done()
        return

    users = await get_users_nearly(
        phone_number=accounts[0].phone_number,
        latitude=location.latitude,
        longitude=location.longitude,
    )

    receivers = get_receivers_from_users(users)

    if not receivers:
        await message.answer(cpt_txt.RECEIVERS_GEO_NO_USERS)
        return

    manager.dialog_data['receivers'] = receivers
    await manager.switch_to(MailingStatesGroup.final_info)


async def cancel_receivers(callback: CallbackQuery, button: Button,
                           manager: DialogManager):
    del manager.dialog_data['receivers']
    await manager.back()
