from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request, Response
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from app.routers import bandwidth, clients, details, summary, uptime, weights
from app.services.onionoo_client import OnionooClient, UpstreamError


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.onionoo = OnionooClient()
        try:
            yield
        finally:
            await app.state.onionoo.aclose()

    app = FastAPI(
        title="Onionoo FastAPI Proxy",
        version="0.1.0",
        description="Semantic/OpenAPI proxy for Tor Onionoo (data is fetched from Onionoo upstream).",
        lifespan=lifespan,
    )

    # Add GZip compression middleware for responses larger than 1KB
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    @app.get("/healthz", tags=["health"])
    async def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.exception_handler(UpstreamError)
    async def upstream_error_handler(_request: Request, exc: UpstreamError) -> Response:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "upstream_error",
                "upstream_status": exc.status_code,
                "upstream_body": exc.body,
            },
        )

    @app.exception_handler(httpx.RequestError)
    async def httpx_error_handler(_request: Request, exc: httpx.RequestError) -> Response:
        return JSONResponse(
            status_code=502,
            content={
                "error": "bad_gateway",
                "message": str(exc),
            },
        )

    app.include_router(summary.router, prefix="/v1", tags=["onionoo"])
    app.include_router(details.router, prefix="/v1", tags=["onionoo"])
    app.include_router(bandwidth.router, prefix="/v1", tags=["onionoo"])
    app.include_router(weights.router, prefix="/v1", tags=["onionoo"])
    app.include_router(clients.router, prefix="/v1", tags=["onionoo"])
    app.include_router(uptime.router, prefix="/v1", tags=["onionoo"])

    return app


app = create_app()
