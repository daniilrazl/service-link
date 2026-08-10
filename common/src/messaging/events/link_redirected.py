from dataclasses import dataclass
from datetime import datetime

from common.src.messaging.constants import ROUTING_KEY_LINK_REDIRECTED
from common.src.messaging.events.base import Event


@dataclass
class LinkRedirected(Event):
    link_id: int
    short_code: str
    timestamp: str

    @property
    def routing_key(self) -> str:
        return ROUTING_KEY_LINK_REDIRECTED
