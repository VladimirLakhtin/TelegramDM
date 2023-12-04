import io

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from src.bot.structures.funcs import standardization_receivers_data
from src.bot.structures.states import ReceiversStatesGroup


async def input_receivers_file(message: Message, widget: MessageInput,
                               manager: DialogManager):
    if message.document.file_name.endswith('.txt'):
        file = await message.bot.get_file(message.document.file_id)
        with io.BytesIO() as file_in_io:
            await message.bot.download_file(file.file_path, file_in_io)
            data = file_in_io.read().decode("latin-1")
        manager.dialog_data['receivers'] = standardization_receivers_data(data)
        await manager.next()
    else:
        await manager.switch_to(ReceiversStatesGroup.from_file)


async def confirm_receivers_file(callback: CallbackQuery, button: Button,
                                 manager: DialogManager):
    await callback.answer('Получатели установлены')
    await manager.switch_to(ReceiversStatesGroup.menu)


async def cancel_receivers_file(callback: CallbackQuery, button: Button,
                                manager: DialogManager):
    del manager.dialog_data['receivers']
    await manager.back()

