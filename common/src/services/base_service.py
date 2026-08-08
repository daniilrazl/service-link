from abc import ABC

from loguru import logger
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from common.src.repositories import BaseRepository

class BaseService[T: DeclarativeBase](ABC):
    repo: BaseRepository[T]

    async def get_all(self, session: AsyncSession) -> list[T]:
        logger.debug("Getting all objects", extra={"model": self.repo.model.__name__})
        
        return await self.repo.get_all(session)
    
    async def get_by_id(self, session: AsyncSession, id: int) -> T | None:
        obj = await self.repo.get_by_id(session, id)
        if obj is None:
            logger.warning("Object not found", extra={"id": id})

        return obj
    
    async def create(self, session: AsyncSession, data: BaseModel) -> T:
        obj = await self.repo.create(session, **data.model_dump())
        await session.commit()
        await session.refresh(obj)
        logger.info("Object created", extra={"model": self.repo.model.__name__})

        return obj
    
    async def update(self, session: AsyncSession, id: int, data: BaseModel) -> T:
        obj = await self.repo.get_by_id(session, id)
        if obj is None:
            logger.warning(
                "Object not found for update",
                extra={"model": self.repo.model.__name__, "id": id}
            )

            return None
        
        await self.repo.update(session, obj, **data.model_dump(exclude_unset=True))
        await session.commit()
        await session.refresh(obj)
        logger.info("Object updated", extra={"model": self.repo.model.__name__, "id": obj.id})

        return obj


    async def delete(self, session: AsyncSession, id: int) -> bool:
        obj = await self.repo.get_by_id(session, id)
        if obj is None:
            logger.warning(
                "Object not found for delete",
                extra={"model": self.repo.model.__name__, "id": id},
            )
            return False

        await self.repo.delete(session, obj)
        await session.commit()
        logger.info("Object deleted", extra={"model": self.repo.model.__name__, "id": id})
        return True