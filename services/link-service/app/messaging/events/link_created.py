from dataclasses import dataclass

from app.messaging.constants import ROUTING_KEY_LINK_CREATED
from app.messaging.events.base import Event


@dataclass
class LinkCreated(Event):
    link_id: int
    short_code: str
    original_url: str

    @property
    def routing_key(self) -> str:
        return ROUTING_KEY_LINK_CREATED
