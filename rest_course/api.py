# PEP 585
from collections.abc import Iterable

from fastapi import FastAPI, HTTPException, Request, Response, status

from . import bdb_manager
from .params import BDBParams, BDBResponse
from .types import UID
from .util import url_for

app = FastAPI(title="REST Course", description="REST API Course")


@app.post(
    "/bdbs",
    tags=["bdb"],
    operation_id="create_bdb",
    response_model=BDBResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_bdb(req: BDBParams, request: Request, response: Response):
    bdb = bdb_manager.create_bdb(req)

    # TODO: Add fields: created_at
    url = url_for(request, "get_bdb", uid=str(bdb.uid))
    response.headers["location"] = url
    return BDBResponse(bdb=bdb, url=url)


@app.get(
    "/bdbs/{uid}", tags=["bdb"], operation_id="get_bdb", response_model=BDBResponse
)
def get_bdb(uid: UID, request: Request):
    try:
        bdb = bdb_manager.get_bdb(uid)
        url = url_for(request, "get_bdb", uid=str(bdb.uid))
        return BDBResponse(bdb=bdb, url=url)
    except LookupError:
        raise HTTPException(status_code=404)


@app.options(
    "/bdbs/{uid}", include_in_schema=False, status_code=status.HTTP_204_NO_CONTENT
)
def bdb_options(response: Response):
    response.headers["allow"] = ", ".join(["OPTIONS", "GET", "PUT"])


@app.get(
    "/bdbs",
    tags=["bdb"],
    operation_id="get_all_bdbs",
    response_model=Iterable[BDBResponse],
)
def get_all_bdbs(request: Request):
    for bdb in bdb_manager.get_all_bdbs():
        url = url_for(request, "get_bdb", uid=str(bdb.uid))
        yield BDBResponse(bdb=bdb, url=url)


@app.options("/bdbs", include_in_schema=False, status_code=status.HTTP_204_NO_CONTENT)
def bdbs_options(response: Response):
    response.headers["allow"] = ", ".join(["OPTIONS", "GET", "POST"])


@app.get("/")
def index(request: Request):
    return {
        "bdbs": url_for(request, "get_all_bdbs"),
    }


@app.options("/", include_in_schema=False, status_code=status.HTTP_204_NO_CONTENT)
def index_options(response: Response):
    response.headers["allow"] = ", ".join(["OPTIONS", "GET"])
