from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from src.bot.structures.states import MenuStatesGroup
from src.bot.logic.dialogs import router as dialog_router

router = Router()
router.include_router(dialog_router)


@router.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MenuStatesGroup.menu)
