import hashlib
import json

from fastapi import HTTPException, Request, status
from pydantic import HttpUrl
from pydantic.json import pydantic_encoder
from starlette.datastructures import URL


def url_for(request: Request, name: str, **path_params) -> HttpUrl:
    url = URL(request.url_for(name, **path_params))
    return HttpUrl(str(url), scheme=url.scheme, host=url.hostname)


def etag_for(obj) -> str:
    j = json.dumps(obj, default=pydantic_encoder)
    return hashlib.sha1(j.encode()).hexdigest()


def verify_etag_match(request, etag):
    # Forbid updating if none of the etags provided in the request matches the current resource's etag.
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/If-Match

    if_match = request.headers.get("if-match")

    if if_match is None:
        # Any etag is fine
        return

    match_etags = [t.strip(' "') for t in if_match.split(",")]

    if etag not in match_etags:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"Current etag '{etag}' does not match any of {match_etags}",
        )
