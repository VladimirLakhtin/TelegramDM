from aiogram_dialog import DialogManager

from src.db import Database


async def get_message_data(dialog_manager: DialogManager, **kwargs):
    return {
        "title": dialog_manager.dialog_data.get("title"),
        "message": dialog_manager.dialog_data.get("message")
    }


async def get_titles_list(dialog_manager: DialogManager, **kwargs):
    db: Database = dialog_manager.middleware_data.get('db')
    data = await db.message.get_titles()
    return {'items': data}


async def get_message_data_by_id(dialog_manager: DialogManager, **kwargs):
    message_id = dialog_manager.dialog_data.get('message_id')
    db: Database = dialog_manager.middleware_data.get('db')
    data = await db.message.get(message_id)
    return {
        'title': data.title,
        'text': data.text,
    }


async def get_receivers_list(dialog_manager: DialogManager, **kwargs):
    return {
        'receivers': '\n'.join(dialog_manager.dialog_data.get('receivers')[:10])
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
