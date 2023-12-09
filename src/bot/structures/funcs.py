import asyncio
import logging
import math
import re
from pathlib import Path

from aiogram_dialog import SubManager, DialogManager, BaseDialogManager
from aiogram_dialog.widgets.kbd import ManagedCheckbox
from pyrogram import Client
from pyrogram.types import InputPhoneContact, User

from src.config import conf
from src.db import Database


def standardization_receivers_data(string: str) -> list[str]:
    result = string.splitlines()
    result = [
        '+7' + f[-10:]
        if len(f := ''.join(re.findall(r'\d+', rec))) in (10, 11)
        else '@' + re.sub(r'(@|https://t\.me/| )', '', rec)
        for rec in result
    ]
    return result


def open_account_option(data: dict, widget, manager: SubManager) -> bool:
    check: ManagedCheckbox = manager.find("acc_check")
    return check.is_checked()


def check_phone_number(phone_number: str) -> bool:
    finds = ''.join(re.findall(r'\+7\d{10}', phone_number))
    return len(phone_number) == 12 and finds


def calculate_mailing_time(receivers: int, accounts: int) -> str:
    delay = conf.delay
    seconds = math.ceil((receivers - accounts) / accounts) * delay
    result = ''

    h = int(seconds // 3600)
    m = int((seconds - h * 3600) // 60)

    if h:
        result += f'{h} ч '
    if m:
        result += f'{m} мин '

    return result or f'{seconds:.0f} сек'


def create_client(phone_number) -> Client:
    return Client(
        name=phone_number,
        api_id=conf.app.id,
        api_hash=conf.app.hash,
        workdir=conf.app.session_dir,
    )


def delete_session(phone_number):
    filename = phone_number + '.session'
    try:
        Path.unlink(conf.app.session_dir / filename)
    except FileNotFoundError:
        logging.error('Cannot delete: file not found')


async def receivers_process(receivers: list[str], app: Client) -> list[str]:
    rec_phone_numbers = [rec for rec in receivers if rec.startswith('+')]
    rec_usernames = [rec for rec in receivers if rec.startswith('@')]

    await app.import_contacts([
        InputPhoneContact(phone=rec_phone_number, first_name=rec_phone_number)
        for rec_phone_number in rec_phone_numbers
    ])
    contacts = await app.get_contacts()

    contacts_ids = [
        contact.id
        for contact in contacts
        if f'+{contact.phone_number}' in rec_phone_numbers
    ]
    return rec_usernames + contacts_ids


async def start_mailing_task(
        manager: BaseDialogManager,
        phone_number: str,
        text: str,
        receivers: list[str],
        is_main: bool = False,
):
    async with create_client(phone_number) as app:
        receivers = await receivers_process(receivers, app)
        for i, receiver in enumerate(receivers):    # type: int, str | int
            await app.send_message(receiver, text)
            if is_main:
                await manager.update(
                    {'progress': (i + 1) / len(receivers) * 100}
                )
            await asyncio.sleep(10)


async def start_mailing_main(
        manager: BaseDialogManager,
        accounts: list[str],
        receivers: list[str],
        message_text: str,
):
    await asyncio.sleep(5)
    tasks = []
    for i, acc in enumerate(accounts):  # type: int, Account
        part = math.ceil(len(receivers) / len(accounts))
        start_acc_receivers = part * i
        end_acc_receivers = part * (i + 1)
        acc_receivers = receivers[start_acc_receivers:end_acc_receivers]
        task = asyncio.create_task(start_mailing_task(
            manager=manager,
            phone_number=acc.phone_number,
            receivers=acc_receivers,
            text=message_text,
            is_main=i == 0,
        ))
        tasks.append(task)

    await manager.update({'tasks': tasks})
    for task in tasks:
        await task
        task.done()

    await manager.done()


if __name__ == '__main__':
    print(calculate_mailing_time(3, 2))
