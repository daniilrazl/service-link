from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Link
from common.src.repositories import BaseRepository


class LinkRepository(BaseRepository[Link]):
    model = Link

    async def get_by_short_code(self, session: AsyncSession, short_code: str) -> Link | None:
        result = await session.execute(
            select(self.model).where(self.model.short_code == short_code)
        )

        return result.scalar_one_or_none()
