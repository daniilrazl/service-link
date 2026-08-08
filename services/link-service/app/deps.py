from app.services import LinkService, link_service


async def get_link_service() -> LinkService:
    return link_service
