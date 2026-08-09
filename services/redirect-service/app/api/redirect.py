from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.services import redirect_service

router = APIRouter()


@router.get("/{short_code}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def redirect(
    short_code: str, session: AsyncSession = Depends(get_async_session)
) -> RedirectResponse:
    original_url = await redirect_service.get_original_url(session, short_code)

    if not original_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found",
        )

    return RedirectResponse(url=original_url)
