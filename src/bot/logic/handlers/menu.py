""" Menu handlers file """
from aiogram_dialog import DialogManager


async def close_all_tasks(data, manager: DialogManager):
    tasks = manager.dialog_data.get('tasks', [])
    for task in tasks:
        task.close()
