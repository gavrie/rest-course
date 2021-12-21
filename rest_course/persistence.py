import json
from collections.abc import Iterable

import redis
from pydantic.json import pydantic_encoder

from .types import BDB, UID


def serialize(obj) -> str:
    return json.dumps(obj, default=pydantic_encoder)


def deserialize(data: str):
    return json.loads(data)


red = redis.Redis(decode_responses=True)


def generate_bdb_uid() -> UID:
    return UID(red.incr("bdb_uid"))


def store_bdb(uid: UID, bdb: BDB):
    red.sadd("bdb:all", uid)
    red.set(f"bdb:{uid}", serialize(bdb))


def get_bdb_uids() -> Iterable[UID]:
    cursor = 0
    while True:
        cursor, uids = red.sscan("bdb:all", cursor)
        for u in uids:
            yield UID(u)
        if cursor == 0:
            break


def get_bdb(uid: UID) -> BDB:
    key = f"bdb:{uid}"

    data = red.get(key)
    if data is None:
        raise LookupError

    bdb = BDB(**deserialize(data))
    return bdb
