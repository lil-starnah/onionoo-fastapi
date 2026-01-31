from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request, Response

from app.models.weights import WeightsResponse
from app.routers.params import common_query_params
from app.routers.proxy import get_onionoo_client, proxy_get_json
from app.services.onionoo_client import OnionooClient

router = APIRouter()


@router.get(
    "/weights",
    response_model=WeightsResponse,
    summary="Get relay weights history",
    description=(
        "Proxies Onionoo `/weights`.\n\n"
        "- Upstream: `GET https://onionoo.torproject.org/weights`\n"
        "- Returns path-selection probability/weight histories (relays only).\n\n"
        "Spec: https://metrics.torproject.org/onionoo.html"
    ),
)
async def get_weights(
    request: Request,
    response: Response,
    params: Annotated[dict[str, Any], Depends(common_query_params)],
    client: Annotated[OnionooClient, Depends(get_onionoo_client)],
) -> WeightsResponse | Response:
    return await proxy_get_json(
        method="weights",
        model=WeightsResponse,
        request=request,
        response=response,
        client=client,
        params=params,
    )
