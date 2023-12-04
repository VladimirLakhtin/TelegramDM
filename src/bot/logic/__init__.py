from aiogram import Router

from .handlers import router as handlers_router
from .dialogs import router as dialogs_router

router = Router()
router.include_routers(handlers_router,)
