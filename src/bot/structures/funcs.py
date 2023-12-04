import logging
import re
from pathlib import Path

from aiogram_dialog import SubManager
from aiogram_dialog.widgets.kbd import ManagedCheckbox
from pyrogram import Client

from src.config import conf


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
