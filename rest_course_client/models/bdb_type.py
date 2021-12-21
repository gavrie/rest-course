from enum import Enum


class BDBType(str, Enum):
    REDIS = "redis"
    MEMCACHED = "memcached"

    def __str__(self) -> str:
        return str(self.value)
