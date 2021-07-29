from pydantic.dataclasses import dataclass

from .types import BDBType


@dataclass
class BDBParams:
    name: str
    memory_size: int
    type: BDBType = BDBType.REDIS
