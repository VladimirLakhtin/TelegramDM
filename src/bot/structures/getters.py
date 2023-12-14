""" Dialogs getters file """
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId

from src.bot.structures.funcs import get_mailing_time
from src.db import Database


async def get_message_data(dialog_manager: DialogManager, **kwargs):
    file_id, file_unique_id, content_type = (
        dialog_manager.dialog_data.get('media', (None, None, None)))
    media = None
    if file_id:
        media = MediaAttachment(
            file_id=MediaId(file_id, file_unique_id),
            type=content_type,
        )
    return {
        "title": dialog_manager.dialog_data.get("title"),
        "message": dialog_manager.dialog_data.get("message"),
        'media': media,
    }


async def get_messages_data(dialog_manager: DialogManager, **kwargs):
    db: Database = dialog_manager.middleware_data.get('db')
    data = await db.message.get_many()
    return {'messages': data}


async def get_message_data_by_id(dialog_manager: DialogManager, **kwargs):
    message_id = dialog_manager.dialog_data.get('message_id')
    db: Database = dialog_manager.middleware_data.get('db')
    message = await db.message.get(message_id)
    media = None
    if message.media_path:
        media = MediaAttachment(
            path=message.media_path,
            type=message.content_type,
        )
    return {
        'message': message,
        'media': media,
    }


async def get_receivers_list(dialog_manager: DialogManager, **kwargs):
    receivers = dialog_manager.dialog_data.get('receivers')
    return {
        'receivers': receivers and '\n'.join(receivers[:10])
    }


async def get_accounts_data(dialog_manager: DialogManager, **kwargs):
    db: Database = dialog_manager.middleware_data.get('db')
    accounts = await db.account.get_all()
    return {'accounts': accounts}


async def get_account_phone_number(dialog_manager: DialogManager, **kwargs):
    db: Database = dialog_manager.middleware_data.get('db')
    account_id = dialog_manager.dialog_data.get('account_id')
    account = await db.account.get(account_id)
    return {'phone_number': account.phone_number}


async def get_final_info(dialog_manager: DialogManager, **kwargs):
    accounts = dialog_manager.start_data.get('accounts')
    receivers = dialog_manager.dialog_data.get('receivers')

    if not receivers:
        return ''

    accounts_text = '\n'.join(
        account.first_name + ' ' + account.phone_number
        for account in accounts
    )
    sending_time = get_mailing_time(len(receivers), len(accounts))

    return {
        'accounts': accounts_text,
        'receivers_count': len(receivers),
        'time': sending_time,
    }


async def get_progress_value(dialog_manager: DialogManager, **kwargs):
    return {
        'progress': dialog_manager.dialog_data.get('progress', 0)
    }
