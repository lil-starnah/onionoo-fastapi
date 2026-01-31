from __future__ import annotations

from datetime import date
from typing import Annotated, Any

from fastapi import Query


def _bool_str(v: bool) -> str:
    return "true" if v else "false"


def common_query_params(
    type: Annotated[str | None, Query(description="relay or bridge")] = None,
    running: Annotated[bool | None, Query(description="true or false")] = None,
    search: Annotated[str | None, Query()] = None,
    lookup: Annotated[str | None, Query()] = None,
    country: Annotated[str | None, Query()] = None,
    as_: Annotated[str | None, Query(alias="as")] = None,
    as_name: Annotated[str | None, Query()] = None,
    flag: Annotated[str | None, Query()] = None,
    first_seen_days: Annotated[str | None, Query()] = None,
    last_seen_days: Annotated[str | None, Query()] = None,
    first_seen_since: Annotated[date | None, Query()] = None,
    last_seen_since: Annotated[date | None, Query()] = None,
    version: Annotated[str | None, Query()] = None,
    os: Annotated[str | None, Query()] = None,
    recommended_version: Annotated[bool | None, Query()] = None,
    order: Annotated[str | None, Query()] = None,
    offset: Annotated[int | None, Query(ge=0)] = None,
    limit: Annotated[int | None, Query(ge=0)] = None,
) -> dict[str, Any]:
    """
    Common Onionoo query parameters (documented in Onionoo spec).

    We convert some types (bool/date) to the string representation Onionoo expects.
    """

    params: dict[str, Any] = {}
    if type is not None:
        params["type"] = type
    if running is not None:
        params["running"] = _bool_str(running)
    if search is not None:
        params["search"] = search
    if lookup is not None:
        params["lookup"] = lookup
    if country is not None:
        params["country"] = country
    if as_ is not None:
        params["as"] = as_
    if as_name is not None:
        params["as_name"] = as_name
    if flag is not None:
        params["flag"] = flag
    if first_seen_days is not None:
        params["first_seen_days"] = first_seen_days
    if last_seen_days is not None:
        params["last_seen_days"] = last_seen_days
    if first_seen_since is not None:
        params["first_seen_since"] = first_seen_since.isoformat()
    if last_seen_since is not None:
        params["last_seen_since"] = last_seen_since.isoformat()
    if version is not None:
        params["version"] = version
    if os is not None:
        params["os"] = os
    if recommended_version is not None:
        params["recommended_version"] = _bool_str(recommended_version)
    if order is not None:
        params["order"] = order
    if offset is not None:
        params["offset"] = str(offset)
    if limit is not None:
        params["limit"] = str(limit)
    return params
