from enum import Enum

from pydantic.dataclasses import dataclass


class UID(int):
    pass


class BDBType(str, Enum):
    REDIS = "redis"
    MEMCACHED = "memcached"


@dataclass
class BDB:
    uid: UID
    name: str
    memory_size: int
    type: BDBType
