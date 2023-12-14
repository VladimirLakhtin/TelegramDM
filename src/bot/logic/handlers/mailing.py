import asyncio

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy import true

from src.bot.structures.funcs import clear_accounts_on_auth
from src.bot.structures.pyrogram_funcs import start_mailing_main, create_client
from src.bot.structures.states import MailingStatesGroup, MenuStatesGroup
from src.bot.structures.text import CaptureText as cpt_txt
from src.db import Database, Account


async def init_mailing_handler(callback: CallbackQuery, button: Button,
                               manager: DialogManager):
    db: Database = manager.middleware_data.get('db')
    accounts = await db.account.get_many(Account.is_ready == true())

    if not accounts:
        await callback.answer(cpt_txt.MAILING_NO_ACCOUNTS)
        return

    await manager.start(
        state=MailingStatesGroup.mes_choose_lst,
        data={'accounts': list(accounts)},
    )


async def choose_message(callback: CallbackQuery, button: Button,
                         manager: DialogManager, item_id: str):
    manager.dialog_data['message_id'] = item_id
    await manager.next()


async def restart_final_info(callback: CallbackQuery, manager: DialogManager,
                             db: Database, no_auth_accounts: list[Account]):
    chat_id = callback.from_user.id
    for acc in no_auth_accounts:
        manager.start_data['accounts'].remove(acc)
        await db.account.delete(acc.id)
        text = cpt_txt.ACCOUNTS_DELETED_ON_AUTH.format(
            first_name=acc.first_name, phone_number=acc.phone_number)
        await callback.bot.send_message(chat_id, text)

    accounts = manager.start_data.get('accounts')
    if not accounts:
        await callback.bot.send_message(chat_id, cpt_txt.MAILING_NO_ACCOUNTS)
        await manager.done(show_mode=ShowMode.SEND)
    else:
        await callback.bot.send_message(chat_id, cpt_txt.FINAL_INFO_UPDATE)
        await manager.switch_to(MailingStatesGroup.final_info, show_mode=ShowMode.SEND)


async def start_mailing_handler(callback: CallbackQuery, button: Button,
                                manager: DialogManager):
    db: Database = manager.middleware_data.get('db')
    accounts = manager.start_data.get('accounts')
    no_auth_accounts = await clear_accounts_on_auth(accounts)
    if no_auth_accounts:
        await restart_final_info(callback, manager, db, no_auth_accounts)
        return

    receivers = manager.dialog_data.get('receivers')
    message_id = manager.dialog_data.get('message_id')
    message = await db.message.get(message_id)

    asyncio.create_task(start_mailing_main(
        manager.bg(),
        accounts,
        receivers,
        message,
    ))

    await manager.next()


async def stop_mailing_handler(callback: CallbackQuery, button: Button,
                               manager: DialogManager):
    tasks = manager.dialog_data.get('tasks')
    for task in tasks:
        task.cancel()
