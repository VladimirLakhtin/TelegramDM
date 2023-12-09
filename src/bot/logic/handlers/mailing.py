import asyncio
import math
from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, Data
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy import true

from src.bot.structures.funcs import start_mailing_task, start_mailing_main
from src.bot.structures.states import MailingStatesGroup, MenuStatesGroup
from src.bot.structures.text import CapturesText as cpt_txt
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


async def start_mailing_handler(callback: CallbackQuery, button: Button,
                                manager: DialogManager):
    await manager.next()

    db: Database = manager.middleware_data.get('db')
    accounts = manager.start_data.get('accounts')
    receivers = manager.dialog_data.get('receivers')
    message_id = manager.dialog_data.get('message_id')
    message = await db.message.get(message_id)

    asyncio.create_task(start_mailing_main(
        manager.bg(),
        accounts,
        receivers,
        message.text,
    ))


async def stop_mailing_handler(callback: CallbackQuery, button: Button,
                               manager: DialogManager):
    tasks = manager.dialog_data.get('tasks')
    for task in tasks:
        task.cancel()

