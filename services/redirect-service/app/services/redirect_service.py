from datetime import UTC, datetime

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Link
from app.repositories import LinkRepository
from common.src.messaging import EventPublisher, LinkRedirected
from common.src.services import BaseService


class RedirectService(BaseService[Link]):
    repo: LinkRepository = LinkRepository()
    _publisher: EventPublisher | None = None

    def init_publisher(self, publisher: EventPublisher) -> None:
        self._publisher = publisher

    async def get_original_url(
        self,
        session: AsyncSession,
        short_code: str,
    ) -> str | None:
        link = await self.repo.get_by_short_code(session, short_code)

        return link.original_url if link else None

    async def record_redirect(
        self,
        session: AsyncSession,
        short_code: str,
    ) -> None:
        link = await self.repo.get_by_short_code(session, short_code)
        if link is None:
            return

        if self._publisher is None:
            logger.warning("Publisher not initialized, skipped event publish")
            return

        event = LinkRedirected(
            link_id=link.id,
            short_code=link.short_code,
            timestamp=datetime.now(UTC).isoformat(),
        )
        
        try:
            await self._publisher.publish(event)
            logger.info(
                "LinkRedirected event published",
                extra={"short_code": short_code},
            )
        except Exception as e:
            logger.error(
                "Failed to publish LinkRedirected event",
                extra={"short_code": short_code, "error": str(e)},
            )


redirect_service: RedirectService = RedirectService()
