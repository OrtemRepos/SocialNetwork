from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config import config

engine = create_async_engine(config.POSTGRES_URL, future=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


def get_session() -> AsyncSession:
    return async_session_maker()
