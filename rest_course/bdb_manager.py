from collections.abc import Iterable

from . import persistence
from .errors import InvalidOperationError
from .params import BDBParams
from .types import BDB, UID


def create_bdb(req: BDBParams) -> BDB:
    uid = persistence.generate_bdb_uid()

    bdb = BDB(
        uid=uid,
        name=req.name,
        type=req.type,
        memory_size=req.memory_size,
    )

    persistence.store_bdb(uid, bdb)

    return bdb


def update_bdb(uid: UID, bdb: BDB) -> BDB:
    current_bdb = persistence.get_bdb(uid)

    if bdb.uid != current_bdb.uid:
        raise InvalidOperationError("uid cannot be modified")

    if bdb.memory_size < current_bdb.memory_size:
        raise InvalidOperationError("memory_size cannot be less than current value")

    persistence.store_bdb(uid, bdb)
    return bdb


def get_bdb(uid: UID) -> BDB:
    return persistence.get_bdb(uid)


def get_all_bdbs() -> Iterable[BDB]:
    for uid in persistence.get_bdb_uids():
        yield persistence.get_bdb(uid)
