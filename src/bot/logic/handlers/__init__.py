from aiogram import Router

from .main import router as messages_router

router = Router()
router.include_routers(
    messages_router,
)
