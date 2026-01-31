from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request, Response

from app.models.clients import ClientsResponse
from app.routers.params import common_query_params
from app.routers.proxy import get_onionoo_client, proxy_get_json
from app.services.onionoo_client import OnionooClient

router = APIRouter()


@router.get(
    "/clients",
    response_model=ClientsResponse,
    summary="Get bridge clients history",
    description=(
        "Proxies Onionoo `/clients`.\n\n"
        "- Upstream: `GET https://onionoo.torproject.org/clients`\n"
        "- Returns estimated daily number of clients connecting to a bridge (bridges only).\n\n"
        "Spec: https://metrics.torproject.org/onionoo.html"
    ),
)
async def get_clients(
    request: Request,
    response: Response,
    params: Annotated[dict[str, Any], Depends(common_query_params)],
    client: Annotated[OnionooClient, Depends(get_onionoo_client)],
) -> ClientsResponse | Response:
    return await proxy_get_json(
        method="clients",
        model=ClientsResponse,
        request=request,
        response=response,
        client=client,
        params=params,
    )
