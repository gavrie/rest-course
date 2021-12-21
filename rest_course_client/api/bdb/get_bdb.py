from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bdb import BDB
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    uid: int,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/bdbs/{uid}".format(client.base_url, uid=uid)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[BDB, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = BDB.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[BDB, HTTPValidationError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    uid: int,
    *,
    client: Client,
) -> Response[Union[BDB, HTTPValidationError]]:
    """Get Bdb

    Args:
        uid (int):

    Returns:
        Response[Union[BDB, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        uid=uid,
        client=client,
    )

    response = httpx.get(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    uid: int,
    *,
    client: Client,
) -> Optional[Union[BDB, HTTPValidationError]]:
    """Get Bdb

    Args:
        uid (int):

    Returns:
        Response[Union[BDB, HTTPValidationError]]
    """

    return sync_detailed(
        uid=uid,
        client=client,
    ).parsed


async def asyncio_detailed(
    uid: int,
    *,
    client: Client,
) -> Response[Union[BDB, HTTPValidationError]]:
    """Get Bdb

    Args:
        uid (int):

    Returns:
        Response[Union[BDB, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        uid=uid,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    uid: int,
    *,
    client: Client,
) -> Optional[Union[BDB, HTTPValidationError]]:
    """Get Bdb

    Args:
        uid (int):

    Returns:
        Response[Union[BDB, HTTPValidationError]]
    """

    return (
        await asyncio_detailed(
            uid=uid,
            client=client,
        )
    ).parsed
