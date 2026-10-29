from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker)
from sqlalchemy.orm import declarative_base
from contextlib import asynccontextmanager
from fastapi import FastAPI


DATABASE_URL = "sqlite+aiosqlite:///./database.db"

engine = create_async_engine(DATABASE_URL, echo=False)

async_session = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()

async def get_session():
    """FastAPI-зависимость: одна сессия на запрос."""
    async with async_session() as session:
        yield session


@asynccontextmanager
async def lifespan (app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

