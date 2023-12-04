"""User repository file."""

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
        text: str
    ) -> None:
        """Insert a new messages into the database.

        :param title: Mailing messages title
        :param text: Mailing messages text
        """
        await self.session.merge(
            Message(
                title=title,
                text=text,
            )
        )
        await self.session.commit()

    async def get_titles(self):
        """Get many messages titles from the database.

                :return: List of founded titles
                """
        statement = select(self.type_model.title)
        return (await self.session.scalars(statement)).all()
