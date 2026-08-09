from pydantic import BaseModel, HttpUrl


class RedirectInfo(BaseModel):
    original_url: HttpUrl
