import json
from collections.abc import Iterable

import redis
from pydantic.json import pydantic_encoder

from .types import BDB, UID

MAX_BDB_UID = 1_000_000


def serialize(obj) -> str:
    return json.dumps(obj, default=pydantic_encoder)


def deserialize(data: str):
    return json.loads(data)


red = redis.Redis(decode_responses=True)


def generate_bdb_uid() -> UID:
    return UID(red.incr("bdb_uid"))


def store_bdb(uid: UID, bdb: BDB):
    red.zadd("bdb:all", {str(uid): uid})
    red.set(f"bdb:{uid}", serialize(bdb))


def get_bdb_uids(offset: int, limit: int) -> Iterable[UID]:
    for uid in red.zrange(
        "bdb:all",
        start=0,
        end=MAX_BDB_UID,
        byscore=True,
        offset=offset,
        num=limit,
    ):
        yield UID(uid)


def get_bdb(uid: UID) -> BDB:
    key = f"bdb:{uid}"

    data = red.get(key)
    if data is None:
        raise LookupError

    bdb = BDB(**deserialize(data))
    return bdb
