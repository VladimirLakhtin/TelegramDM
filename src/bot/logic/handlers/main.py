"""Main menu handlers file"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from src.bot.structures.states import MenuStatesGroup
from src.bot.logic.dialogs import router as dialog_router
from src.db import Database, Account

router = Router()
router.include_router(dialog_router)


@router.message(Command("start"))
async def start_handler(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MenuStatesGroup.menu)
