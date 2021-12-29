# PEP 585
from collections.abc import Iterable

from fastapi import FastAPI, HTTPException, status

from .params import BDBParams
from .types import BDB, UID

app = FastAPI()

all_bdbs: dict[UID, BDB] = {}
bdb_last_uid = 0


@app.post("/bdbs", status_code=status.HTTP_201_CREATED)
def create_bdb(req: BDBParams) -> BDB:
    global bdb_last_uid
    bdb_last_uid += 1
    uid = UID(bdb_last_uid)

    bdb = BDB(
        uid=uid,
        name=req.name,
        type=req.type,
        memory_size=req.memory_size,
    )

    all_bdbs[uid] = bdb
    return bdb


@app.get("/bdbs/{uid}")
def get_bdb(uid: UID) -> BDB:
    try:
        return all_bdbs[uid]
    except LookupError:
        raise HTTPException(status_code=404)


@app.get("/bdbs")
def get_all_bdbs() -> Iterable[BDB]:
    for uid in all_bdbs:
        yield all_bdbs[uid]
