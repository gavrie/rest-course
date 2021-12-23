# PEP 585
from collections.abc import Iterable

from fastapi import FastAPI, HTTPException, status

from .params import BDBParams
from .types import BDB, UID

app = FastAPI(title="REST Course", description="REST API Course")

all_bdbs: dict[UID, BDB] = {}
bdb_last_uid = 0


@app.post(
    "/bdbs",
    tags=["bdb"],
    operation_id="create_bdb",
    status_code=status.HTTP_201_CREATED,
    response_model=BDB,
)
def create_bdb(req: BDBParams):
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


@app.get("/bdbs/{uid}", tags=["bdb"], operation_id="get_bdb", response_model=BDB)
def get_bdb(uid: UID):
    try:
        return all_bdbs[uid]
    except LookupError:
        raise HTTPException(status_code=404)


@app.get(
    "/bdbs",
    tags=["bdb"],
    operation_id="get_all_bdbs",
    response_model=Iterable[BDB],
)
def get_all_bdbs():
    for uid in all_bdbs:
        yield all_bdbs[uid]
