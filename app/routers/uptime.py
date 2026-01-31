from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request, Response

from app.models.uptime import UptimeResponse
from app.routers.params import common_query_params
from app.routers.proxy import get_onionoo_client, proxy_get_json
from app.services.onionoo_client import OnionooClient

router = APIRouter()


@router.get(
    "/uptime",
    response_model=UptimeResponse,
    summary="Get uptime history",
    description=(
        "Proxies Onionoo `/uptime`.\n\n"
        "- Upstream: `GET https://onionoo.torproject.org/uptime`\n"
        "- Returns fractional uptimes of relays and bridges.\n\n"
        "Spec: https://metrics.torproject.org/onionoo.html"
    ),
)
async def get_uptime(
    request: Request,
    response: Response,
    params: Annotated[dict[str, Any], Depends(common_query_params)],
    client: Annotated[OnionooClient, Depends(get_onionoo_client)],
) -> UptimeResponse | Response:
    return await proxy_get_json(
        method="uptime",
        model=UptimeResponse,
        request=request,
        response=response,
        client=client,
        params=params,
    )
