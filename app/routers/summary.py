from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request, Response

from app.models.summary import SummaryResponse
from app.routers.params import common_query_params
from app.routers.proxy import get_onionoo_client, proxy_get_json
from app.services.onionoo_client import OnionooClient

router = APIRouter()


@router.get(
    "/summary",
    response_model=SummaryResponse,
    summary="Get relay/bridge summary (semantic)",
    description=(
        "Proxies Onionoo `/summary` and returns a semantic response.\n\n"
        "- Upstream: `GET https://onionoo.torproject.org/summary`\n"
        "- This API maps Onionoo short keys to semantic fields:\n"
        "  - relay: `n,f,a,r` → `nickname,fingerprint,addresses,running`\n"
        "  - bridge: `n,h,r` → `nickname,hashed_fingerprint,running`\n\n"
        "Spec: https://metrics.torproject.org/onionoo.html"
    ),
)
async def get_summary(
    request: Request,
    response: Response,
    params: Annotated[dict[str, Any], Depends(common_query_params)],
    client: Annotated[OnionooClient, Depends(get_onionoo_client)],
) -> SummaryResponse | Response:
    return await proxy_get_json(
        method="summary",
        model=SummaryResponse,
        request=request,
        response=response,
        client=client,
        params=params,
    )
