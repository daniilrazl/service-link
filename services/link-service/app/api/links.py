from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.deps import get_link_service
from app.models import Link
from app.schemas import LinkCreate, LinkResponse
from app.services import LinkService

router = APIRouter(prefix="/links", tags=["Links"])


@router.post("", response_model=LinkResponse)
async def create_link(
    data: LinkCreate,
    session: AsyncSession = Depends(get_async_session),
    service: LinkService = Depends(get_link_service),
) -> Link:
    return await service.create_link(session, data)
