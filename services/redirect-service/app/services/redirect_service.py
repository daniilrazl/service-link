from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Link
from app.repositories import LinkRepository
from common.src.services import BaseService


class RedirectService(BaseService[Link]):
    repo: LinkRepository = LinkRepository()

    async def get_original_url(
        self,
        session: AsyncSession,
        short_code: str,
    ) -> str | None:
        link = await self.repo.get_by_short_code(session, short_code)

        return link.original_url if link else None


redirect_service: RedirectService = RedirectService()
