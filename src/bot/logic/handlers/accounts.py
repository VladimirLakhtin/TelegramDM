import io

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from pyrogram import Client
from pyrogram.errors import PhoneCodeInvalid, FloodWait, PhoneCodeExpired

from src.bot.structures.funcs import check_phone_number, create_client, delete_session
from src.bot.structures.states import AccountsStatesGroup
from src.bot.structures.text import CapturesText as cpt_txt, ButtonText as btn_txt
from src.db import Database, Account


async def input_phone_number_handler(message: Message, widget: MessageInput,
                                     manager: DialogManager):
    if not check_phone_number(message.text):
        await message.answer(cpt_txt.ACCOUNTS_PHONE_INCORRECT_INPUT)
        await manager.switch_to(AccountsStatesGroup.input_phone_number)
        return

    phone_number = message.text
    client = create_client(message.text)
    await client.connect()
    try:
        sent_code_info = await client.send_code(phone_number)
    except FloodWait as ex:
        await message.answer(cpt_txt.ACCOUNTS_PHONE_INPUT_FLOOD.format(ex.value))
        await client.disconnect()
        delete_session(phone_number)
        await manager.switch_to(AccountsStatesGroup.input_phone_number)
    else:
        manager.dialog_data['client'] = client
        manager.dialog_data['phone_number'] = phone_number
        manager.dialog_data['phone_code_hash'] = sent_code_info.phone_code_hash
        await manager.switch_to(AccountsStatesGroup.input_code)


async def input_phone_code_handler(message: Message, widget: MessageInput,
                                   manager: DialogManager):
    phone_code = message.text
    client: Client = manager.dialog_data.get('client')
    phone_number = manager.dialog_data.get('phone_number')
    phone_code_hash = manager.dialog_data.get('phone_code_hash')

    try:
        await client.sign_in(phone_number, phone_code_hash, phone_code)
    except PhoneCodeInvalid:
        await message.answer(cpt_txt.ACCOUNTS_CODE_INCORRECT_INPUT)
    except PhoneCodeExpired:
        await message.answer(cpt_txt.ACCOUNTS_CODE_EXPIRED_INPUT)
    else:
        me = await client.get_me()
        db: Database = manager.middleware_data.get('db')
        await db.account.new(
            phone_number=phone_number,
            username=me.username,
            first_name=me.first_name,
        )
    finally:
        await client.disconnect()
        await manager.switch_to(AccountsStatesGroup.lst)


async def account_confirm_delete_handler(callback: CallbackQuery, button: Button,
                                 manager: DialogManager):
    manager.dialog_data['account_id'] = manager.item_id
    await manager.switch_to(AccountsStatesGroup.delete)


async def account_delete_handler(callback: CallbackQuery, button: Button,
                                 manager: DialogManager):
    account_id = manager.dialog_data.get('account_id')
    db: Database = manager.middleware_data.get('db')
    await db.account.delete(Account.id == int(account_id))
    await manager.switch_to(AccountsStatesGroup.lst)


async def turn_account_handler(callback: CallbackQuery, button: Button,
                               manager: DialogManager):
    db: Database = manager.middleware_data.get('db')
    await db.account.change_ready_status(account_id=manager.item_id)
