import math
import re

from aiogram_dialog import SubManager, DialogManager
from aiogram_dialog.widgets.kbd import ManagedCheckbox

from src.bot.structures.pyrogram_funcs import get_chat_members, create_client
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


async def get_receivers_from_chat(phone_numbers: str, chatname: str) -> list[str]:
    members = await get_chat_members(phone_numbers, chatname)
    return [
        '@' + u if u else '+' + p
        for chat in members
        if not chat.user.is_bot and
           ((u := chat.user.username) or (p := chat.user.phone_number))
    ]


async def clear_accounts_on_auth(accounts: list[Account]) -> list[Account]:
    result = []
    for acc in accounts:    #type: Account
        client = create_client(acc.phone_number)
        is_auth = await client.connect()
        await client.disconnect()
        if not is_auth:
            result.append(acc)
    return result



if __name__ == '__main__':
    print(calculate_mailing_time(3, 2))
