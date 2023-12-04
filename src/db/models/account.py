"""Account model file."""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Account(Base):
    """Telegram account model."""

    phone_number: Mapped[str] = mapped_column(String(12))
    first_name: Mapped[str]
    is_ready: Mapped[bool] = mapped_column(default=False)
    username: Mapped[str | None]
