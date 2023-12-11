"""Init aiogram dialogs file"""
from aiogram import Router

from .main import dialog as main_dialog
from .mailing import dialog as mailing_dialog
from .accounts import dialog as accounts_dialog
from .messages import dialog as messages_dialog

router = Router()
router.include_routers(
    main_dialog,
    mailing_dialog,
    accounts_dialog,
    messages_dialog,
)
