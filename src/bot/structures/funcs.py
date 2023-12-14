""" Other functions file """
import math
import random
import re
import string

from aiogram_dialog import SubManager
from aiogram_dialog.widgets.kbd import ManagedCheckbox
from pyrogram.errors import AuthKeyUnregistered
from pyrogram.raw.functions.updates import GetState
from pyrogram.types import User, ChatMember

from src.bot.structures.pyrogram_funcs import create_client
from src.config import conf
from src.db import Account


def standardization_receivers_data(string: str) -> list[str]:
    result = string.splitlines()
    result = [
        '+7' + f[-10:]
        if len(f := ''.join(re.findall(r'\d+', rec))) in (10, 11)
        else '@' + re.sub(r'(@|https://t\.me/| )', '', rec)
        for rec in result
    ]
    return result


def get_slug() -> str:
    """ Get random string """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(15))


def open_account_option(data: dict, widget, manager: SubManager) -> bool:
    check: ManagedCheckbox = manager.find("acc_check")
    return check.is_checked()


def check_phone_number(phone_number: str) -> bool:
    """ Phone number validate """
    finds = ''.join(re.findall(r'\+7\d{10}', phone_number))
    return len(phone_number) == 12 and finds


def get_mailing_time(receivers: int, accounts: int) -> str:
    """ Calculate mailing time """
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


def get_receivers_from_members(users: list[ChatMember]):
    """ Get receivers usernames or phone numbers from ChatMember instances """
    return [
        '@' + u if u else '+' + p
        for chat in users
        if not chat.user.is_bot and
           ((u := chat.user.username) or (p := chat.user.phone_number))
    ]


def get_receivers_from_users(users: list[User]):
    """ Get receivers usernames or phone numbers from User instances """
    return [
        '@' + u if u else '+' + p
        for chat in users
        if not chat.bot and
           ((u := chat.username) or (p := chat.phone))
    ]


async def clear_accounts_on_auth(accounts: list[Account]) -> list[Account]:
    """ Searches for non-authenticated accounts """
    result = []
    for acc in accounts:    # type: Account
        client = create_client(acc.phone_number)
        is_auth = await client.connect()
        if not is_auth:
            result.append(acc)
            await client.disconnect()
            continue
        try:
            await client.invoke(GetState())
        except AuthKeyUnregistered:
            result.append(acc)
        await client.disconnect()
    return result


if __name__ == '__main__':
    print(get_mailing_time(3, 2))
