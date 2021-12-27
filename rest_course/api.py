# PEP 585
from collections.abc import Iterable

import yaml
from fastapi import FastAPI, HTTPException, Request, Response

from . import bdb_manager
from .params import BDBParams, BDBResponse
from .types import UID
from .util import url_for

app = FastAPI(title="REST Course", description="REST API Course")


@app.post("/bdbs", tags=["bdb"], operation_id="create_bdb", response_model=BDBResponse)
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
    except LookupError:
        raise HTTPException(status_code=404)

    url = url_for(request, "get_bdb", uid=str(bdb.uid))
    bdb_response = BDBResponse(bdb=bdb, url=url)

    if "yaml" in request.headers["accept"].lower():
        content = yaml.dump(bdb_response)
        return Response(content=content, media_type="application/x-yaml")
    else:
        return bdb_response


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
