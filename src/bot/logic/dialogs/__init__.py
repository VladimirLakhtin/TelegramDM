"""Init aiogram dialogs file"""
from aiogram import Router

from .main import dialog as main_dialog
from .params import dialog as message_dialog
from .accounts import dialog as accounts_dialog
from .messages import dialog as messages_dialog
from .receivers import dialog as receivers_dialog
from ...middlewares.database_md import DatabaseMiddleware

router = Router()
router.include_routers(
    main_dialog,
    message_dialog,
    accounts_dialog,
    messages_dialog,
    receivers_dialog,
)
