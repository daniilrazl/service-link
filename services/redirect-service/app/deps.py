from app.services import RedirectService, redirect_service


async def get_redirect_service() -> RedirectService:
    return redirect_service
