from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query, Request, Response

from app.models.details import DetailsResponse
from app.routers.params import common_query_params
from app.routers.proxy import get_onionoo_client, proxy_get_json
from app.services.onionoo_client import OnionooClient

router = APIRouter()


@router.get(
    "/details",
    response_model=DetailsResponse,
    summary="Get relay/bridge details",
    description=(
        "Proxies Onionoo `/details`.\n\n"
        "- Upstream: `GET https://onionoo.torproject.org/details`\n"
        "- Supports Onionoo query parameters (e.g. `search`, `lookup`, `running`, `limit`, ...)\n"
        "- Supports `fields` (details-only) to limit returned top-level fields\n\n"
        "Spec: https://metrics.torproject.org/onionoo.html"
    ),
)
async def get_details(
    request: Request,
    response: Response,
    params: Annotated[dict[str, Any], Depends(common_query_params)],
    fields: Annotated[
        str | None,
        Query(
            description=(
                "Comma-separated list of top-level fields to include (details only). "
                "All other fields will be removed from the response."
            ),
        ),
    ] = None,
    client: Annotated[OnionooClient, Depends(get_onionoo_client)] = None,
) -> DetailsResponse | Response:
    if fields is not None:
        params["fields"] = fields

    return await proxy_get_json(
        method="details",
        model=DetailsResponse,
        request=request,
        response=response,
        client=client,
        params=params,
    )
