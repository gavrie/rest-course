from pydantic.dataclasses import dataclass

from .types import BDBType, BDB

Url = str


@dataclass
class BDBParams:
    name: str
    memory_size: int
    type: BDBType = BDBType.REDIS


@dataclass
class BDBResponse:
    bdb: BDB
    url: Url
