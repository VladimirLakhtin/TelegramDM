import asyncio
import logging
import math
from pathlib import Path

import pyrogram.errors
from aiogram_dialog import BaseDialogManager
from pyrogram import Client
from pyrogram.errors import AuthRestart
from pyrogram.types import User, InputPhoneContact, Chat, ChatMember
from pyrogram.raw.functions.contacts import GetLocated
from pyrogram.raw.types import InputGeoPoint

from src.config import conf
from src.db import Account


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
    client = create_client(phone_number)
    is_authorized = await client.connect()
    await client.disconnect()

    if not is_authorized:
        raise pyrogram.errors.AuthRestart

    async with client as app:
        receivers = await receivers_process(receivers, app)
        for i, receiver in enumerate(receivers):    # type: int, str | int
            await app.send_message(receiver, text)
            if is_main:
                await manager.update(
                    {'progress': (i + 1) / len(receivers) * 100}
                )
            await asyncio.sleep(conf.delay)


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
        acc_receivers = receivers[part * i:part * (i + 1)]
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
        try:
            await task
        except AuthRestart:
            pass
        finally:
            task.done()

    await manager.done()


async def get_chat_members(phone_number: str, chat_id: int | str) -> list[ChatMember]:
    async with create_client(phone_number) as app:
        return [member async for member in app.get_chat_members(chat_id)]


# async def get_nearby_chats(session_name, latitude, longitude):
#     async with Client(session_name, API_ID, API_HASH) as app:
#         return await app.get_nearby_chats(latitude, longitude)
#
async def get_users_nearly(phone_number: str, latitude: float, longitude: float) -> list[User]:
    async with create_client(phone_number) as app:
        geo = InputGeoPoint(lat=latitude, long=longitude, accuracy_radius=1)
        located = GetLocated(geo_point=geo, self_expires=42)
        result = await app.invoke(located)
        return result.users


if __name__ == '__main__':
    LATITUDE = 45.02818292685331
    LONGITUDE = 38.971911885422664
    accs = asyncio.run(get_users_nearly('+79528151052', LATITUDE, LONGITUDE))
    print(accs)
