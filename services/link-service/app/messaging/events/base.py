from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass


@dataclass
class Event(ABC):
    @property
    @abstractmethod
    def routing_key(self) -> str: ...

    def to_dict(self) -> dict:
        return asdict(self)
