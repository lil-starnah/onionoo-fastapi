from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request, Response

from app.models.clients import ClientsResponse
from app.routers.params import common_query_params
from app.routers.proxy import get_onionoo_client, proxy_get_json
from app.services.onionoo_client import OnionooClient

router = APIRouter()


@router.get("/clients", response_model=ClientsResponse)
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
