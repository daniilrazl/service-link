from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


class BaseRepository[T: DeclarativeBase]:
    model: type[T]

    async def get_all(self, session: AsyncSession) -> list[T]:
        result = await session.execute(select(self.model))

        return list(result.scalars().all())

    async def get_by_id(self, session: AsyncSession, id: int) -> T | None:
        result = await session.execute(select(self.model).where(self.model.id == id))

        return result.scalar_one_or_none()

    async def create(self, session: AsyncSession, **kwargs) -> T:
        obj = self.model(**kwargs)
        session.add(obj)

        return obj

    async def update(self, session: AsyncSession, obj: T, **kwargs) -> T:
        for key, value in kwargs.items():
            if value is not None:
                setattr(obj, key, value)

        return obj

    async def delete(self, session: AsyncSession, obj: T) -> None:
        await session.delete(obj)
