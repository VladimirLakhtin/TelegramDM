"""Database class with all-in-one features."""

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine

from src.config import conf

from .repositories import MessageRepo, AccountRepo


def create_async_engine(url: URL | str) -> AsyncEngine:
    """Create async engine with given URL.

    :param url: URL to connect
    :return: AsyncEngine
    """
    return _create_async_engine(url=url, echo=conf.debug, pool_pre_ping=True)


class Database:
    """Database class.

    is the highest abstraction level of database and
    can be used in the handlers or any others bot-side functions.
    """

    message: MessageRepo
    """ Message repository """
    account: AccountRepo
    """ Account repository """

    session: AsyncSession

    def __init__(
        self,
        session: AsyncSession,
        message: MessageRepo = None,
        account: AccountRepo = None,
    ):
        """Initialize Database class.

        :param session: AsyncSession to use
        :param message: (Optional) Message repository
        :param account: (Optional) Account repository
        """
        self.session = session
        self.message = message or MessageRepo(session=session)
        self.account = account or AccountRepo(session=session)
