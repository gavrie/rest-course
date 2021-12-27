from fastapi import Request
from pydantic import HttpUrl
from starlette.datastructures import URL


def url_for(request: Request, name: str, **path_params) -> HttpUrl:
    url = URL(request.url_for(name, **path_params))
    return HttpUrl(str(url), scheme=url.scheme, host=url.hostname)
