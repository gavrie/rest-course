from enum import Enum

from pydantic import PositiveInt
from pydantic.dataclasses import dataclass


class UID(PositiveInt):
    pass


class BDBType(str, Enum):
    REDIS = "redis"
    MEMCACHED = "memcached"


@dataclass
class BDB:
    uid: UID
    name: str
    memory_size: PositiveInt
    type: BDBType
