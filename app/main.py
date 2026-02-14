import httpx
from fastapi import FastAPI, Request, Response
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from app.routers import bandwidth, clients, details, summary, uptime, weights
from app.services.onionoo_client import UpstreamError

# Paths that must not be gzip-compressed so clients (e.g. Swagger UI in Workers) get plain JSON
_OPENAPI_NO_GZIP_PATHS = ("/openapi.json",)


def _no_gzip_openapi_middleware(app: ASGIApp) -> ASGIApp:
    """Strip Accept-Encoding for OpenAPI path so GZip won't compress (fixes /docs in Workers)."""

    async def middleware(scope: Scope, receive: Receive, send: Send) -> None:
        if scope.get("type") == "http" and scope.get("path") in _OPENAPI_NO_GZIP_PATHS:
            scope = dict(scope)
            scope["headers"] = [
                (k, v)
                for k, v in scope.get("headers", [])
                if k.lower() != b"accept-encoding"
            ]
        await app(scope, receive, send)

    return middleware


class _NoGzipOpenAPIMiddleware:
    """ASGI middleware wrapper so add_middleware() can use the function above."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = _no_gzip_openapi_middleware(app)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await self.app(scope, receive, send)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Onionoo FastAPI Proxy",
        version="0.1.0",
        description="Semantic/OpenAPI proxy for Tor Onionoo (data is fetched from Onionoo upstream).",
    )

    def custom_openapi():
        if app.openapi_schema is not None:
            return app.openapi_schema
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version or "0.1.0",
            description=app.description,
            routes=app.routes,
            openapi_version="3.0.2",
        )
        return app.openapi_schema

    app.openapi = custom_openapi

    # Add GZip compression middleware for responses larger than 1KB
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    # Serve /openapi.json uncompressed so Swagger UI works (e.g. in Cloudflare Workers)
    app.add_middleware(_NoGzipOpenAPIMiddleware)

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
