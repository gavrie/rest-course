from pydantic import HttpUrl, PositiveInt
from pydantic.dataclasses import dataclass

from .types import BDB, BDBType


@dataclass
class BDBParams:
    name: str
    memory_size: PositiveInt
    type: BDBType = BDBType.REDIS


@dataclass
class BDBResponse:
    bdb: BDB
    url: HttpUrl


@dataclass
class EventResponse:
    uuid: str
    url: HttpUrl
