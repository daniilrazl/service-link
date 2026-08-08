from pydantic import BaseModel, ConfigDict, HttpUrl


class LinkCreate(BaseModel):
    original_url: HttpUrl


class LinkResponse(BaseModel):
    id: int
    short_code: str
    original_url: str

    model_config = ConfigDict(from_attributes=True)
