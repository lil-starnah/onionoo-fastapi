from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any, TypeVar

from fastapi import HTTPException, Request, Response
from pydantic import BaseModel

from app.services.onionoo_client import OnionooClient

ModelT = TypeVar("ModelT", bound=BaseModel)


async def get_onionoo_client() -> AsyncGenerator[OnionooClient, None]:
    """Request-scoped Onionoo client (create per request, close after)."""
    client = OnionooClient()
    try:
        yield client
    finally:
        await client.aclose()


async def proxy_get_json(
    *,
    method: str,
    model: type[ModelT],
    request: Request,
    response: Response,
    client: OnionooClient,
    params: dict[str, Any],
) -> ModelT | Response:
    if_modified_since = request.headers.get("if-modified-since")
    upstream = await client.get(method=method, params=params, if_modified_since=if_modified_since)

    last_modified = upstream.headers.get("last-modified")

    if upstream.status_code == 304:
        headers: dict[str, str] = {}
        if last_modified:
            headers["Last-Modified"] = last_modified
        return Response(status_code=304, headers=headers)

    if last_modified:
        response.headers["Last-Modified"] = last_modified

    if upstream.json_body is None:
        # This should not happen for Onionoo, but we keep a defensive error.
        raise HTTPException(status_code=502, detail="Upstream did not return JSON")

    return model.model_validate(upstream.json_body)
