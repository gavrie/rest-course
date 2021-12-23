from pydantic import PositiveInt
from pydantic.dataclasses import dataclass

from .types import BDBType


@dataclass
class BDBParams:
    name: str
    memory_size: PositiveInt
    type: BDBType = BDBType.REDIS
