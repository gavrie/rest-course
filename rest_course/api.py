# PEP 585
from collections.abc import Iterable

from fastapi import FastAPI, HTTPException

from . import bdb_manager
from .params import BDBParams
from .types import BDB, UID

app = FastAPI()


@app.post("/bdbs")
def create_bdb(req: BDBParams) -> BDB:
    bdb = bdb_manager.create_bdb(req)
    return bdb


@app.get("/bdbs/{uid}")
def get_bdb(uid: UID) -> BDB:
    try:
        return bdb_manager.get_bdb(uid)
    except LookupError:
        raise HTTPException(status_code=404)


@app.get("/bdbs")
def get_all_bdbs() -> Iterable[BDB]:
    return bdb_manager.get_all_bdbs()
