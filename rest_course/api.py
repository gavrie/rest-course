# PEP 585
from collections.abc import Iterable

from fastapi import FastAPI, HTTPException, status

from . import bdb_manager
from .params import BDBParams
from .types import BDB, UID

app = FastAPI(title="REST Course", description="REST API Course")


@app.post(
    "/bdbs",
    tags=["bdb"],
    operation_id="create_bdb",
    status_code=status.HTTP_201_CREATED,
    response_model=BDB,
)
def create_bdb(req: BDBParams):
    bdb = bdb_manager.create_bdb(req)
    return bdb


@app.get("/bdbs/{uid}", tags=["bdb"], operation_id="get_bdb", response_model=BDB)
def get_bdb(uid: UID):
    try:
        return bdb_manager.get_bdb(uid)
    except LookupError:
        raise HTTPException(status_code=404)


@app.get(
    "/bdbs",
    tags=["bdb"],
    operation_id="get_all_bdbs",
    response_model=Iterable[BDB],
)
def get_all_bdbs():
    return bdb_manager.get_all_bdbs()
