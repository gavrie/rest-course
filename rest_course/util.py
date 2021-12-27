from fastapi import Request
from pydantic import HttpUrl
from starlette.datastructures import URL


def url_for(request: Request, name: str, query_params=None, **path_params) -> HttpUrl:
    if query_params is None:
        query_params = {}

    url = URL(request.url_for(name, **path_params))
    url = url.include_query_params(**query_params)
    return HttpUrl(str(url), scheme=url.scheme, host=url.hostname)


def link(rels):
    """
    Build a Link header: https://www.w3.org/wiki/LinkHeader

    Example:
        <http://localhost:8000/bdbs?offset=0&limit=10>; rel="first",
        <http://localhost:8000/bdbs?offset=40&limit=10>; rel="prev",
        <http://localhost:8000/bdbs?offset=50&limit=10>; rel="next",
        <http://localhost:8000/bdbs?offset=90&limit=10>; rel="last"
    """

    sep = ", "
    link = sep.join(f'<{url}>; rel="{rel}"' for rel, url in rels.items())
    return link
