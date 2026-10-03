from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

from sqlalchemy.orm import DeclarativeBase

from config import settings


# =========================================================
# BASE MODEL
# =========================================================

class Base(DeclarativeBase):
    pass


# =========================================================
# DATABASE ENGINE
# =========================================================

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)


# =========================================================
# SESSION
# =========================================================

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

async def init_database():
    """
    Create all database tables.
    """

    async with engine.begin() as connection:

        await connection.run_sync(
            Base.metadata.create_all
        )


# =========================================================
# DATABASE SESSION
# =========================================================

async def get_db():

    async with AsyncSessionLocal() as session:

        try:
            yield session

        finally:
            await session.close()


# =========================================================
# DATABASE SHUTDOWN
# =========================================================

async def close_database():

    await engine.dispose()
