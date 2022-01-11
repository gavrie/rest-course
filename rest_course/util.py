from fastapi import Request
from starlette.datastructures import URL

from rest_course.params import Url


def url_for(request: Request, name: str, **path_params) -> Url:
    url = URL(request.url_for(name, **path_params))
    return Url(str(url), scheme=url.scheme, host=url.hostname)
