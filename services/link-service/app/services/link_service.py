from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models import Link
from app.repositories import LinkRepository
from app.schemas import LinkCreate
from app.utils import generate_short_code
from common.src.messaging import EventPublisher, LinkCreated
from common.src.services import BaseService


class LinkService(BaseService[Link]):
    repo: LinkRepository = LinkRepository()
    _publisher: EventPublisher | None = None

    def init_publisher(self, publisher: EventPublisher) -> None:
        self._publisher = publisher

    async def get_unique_short_code(self, session: AsyncSession) -> str:
        while True:
            short_code = generate_short_code(settings.short_code_length)
            if not await self.repo.exists_by_short_code(session, short_code):
                return short_code

    async def create_link(self, session: AsyncSession, data: LinkCreate) -> Link:
        short_code = await self.get_unique_short_code(session)

        link = await self.repo.create(
            session,
            original_url=str(data.original_url),
            short_code=short_code,
        )

        await session.commit()
        await session.refresh(link)

        logger.info("Link created", extra={"short_code": short_code})

        if self._publisher:
            event = LinkCreated(
                link_id=link.id,
                short_code=link.short_code,
                original_url=link.original_url,
            )
            await self._publisher.publish(event)

        return link


link_service: LinkService = LinkService()
