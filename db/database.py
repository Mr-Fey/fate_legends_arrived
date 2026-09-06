import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from .repositories import *
from settings import settings 


_log = logging.getLogger(name=__name__)


class Database(UserRepo, ItemRepo, CharacterRepo):
    def __init__(self) -> None:
        self.engine = create_async_engine(
            settings.db_url,
            pool_pre_ping=True,
            echo=False,
        )
        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            autoflush=False,
        )

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            try:
                yield session
            except ValueError: 
                pass 
            except Exception:
                _log.exception("Database Exception")
                raise
            finally:
                await session.close()
