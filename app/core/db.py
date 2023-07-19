from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, declared_attr

from app.core.config import settings


class PreBase:
    """Заготовка для базового класса."""

    @declared_attr
    def __tablename__(cls):
        """Название таблицы возвращает название класса в нижнем регистре."""
        return cls.__name__.lower()

    # всем таблицам по-умолчанию присваивается поле ID
    id = Column(Integer, primary_key=True)


# создаем базовый класс для моделей, с указанием PreBase
Base = declarative_base(cls=PreBase)


class BaseDonationCharityProject(Base):
    __abstract__ = True
    
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)


# асинхронный движок
engine = create_async_engine(settings.database_url)

# множественное создание сессий
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """Асинхронный генератор сессий."""
    # Через асинхронный контекстный менеджер и sessionmaker
    # открывается сессия.
    async with AsyncSessionLocal() as async_session:
        # Генератор с сессией передается в вызывающую функцию.
        yield async_session
        # Когда HTTP-запрос отработает - выполнение кода вернётся сюда,
        # и при выходе из контекстного менеджера сессия будет закрыта.
