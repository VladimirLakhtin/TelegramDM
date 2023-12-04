"""Account repository file."""

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Base, Account
from .abstract import Repository


class AccountRepo(Repository[Account]):
    """Account repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize accounts repository"""
        super().__init__(type_model=Account, session=session)

    async def new(
        self,
        phone_number: str,
        first_name: str,
        username: str = None,
    ) -> None:
        """Insert a new account into the database.

        :param phone_number: Account phone number
        :param first_name: Account first name
        :param username: Account username
        """
        await self.session.merge(
            Account(
                phone_number=phone_number,
                first_name=first_name,
                username=username,
            )
        )
        await self.session.commit()

    async def get_all(self):
        """Get many accounts phone numbers from the database.

                :return: List of founded phone numbers
                """
        statement = select(self.type_model)
        return (await self.session.scalars(statement)).all()

    async def change_ready_status(
            self,
            account_id: int,
    ) -> None:
        account = await self.get(account_id)
        statement = (
            update(self.type_model).
            where(self.type_model.id == account_id).
            values(is_ready=not account.is_ready)
        )
        await self.session.execute(statement)
        await self.session.commit()

