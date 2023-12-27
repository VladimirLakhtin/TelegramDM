"""User repository file."""
import os

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Base, Message
from .abstract import Repository


class MessageRepo(Repository[Message]):
    """Message repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize messages repository"""
        super().__init__(type_model=Message, session=session)

    async def new(
        self,
        title: str,
        text: str,
        content_type: str,
        media_path: str = None,
    ) -> None:
        """Insert a new messages into the database.

        :param title: Mailing message title
        :param text: Mailing message text
        :param media_path: Mailing message media path
        :param content_type: Mailing message media content type
        """
        await self.session.merge(
            Message(
                title=title,
                text=text,
                content_type=content_type,
                media_path=media_path,
            )
        )
        await self.session.commit()

    async def delete(self, id: int) -> None:
        message = await self.get(id)
        if message.media_path:
            os.remove(message.media_path)
        await super().delete(Message.id == id)


