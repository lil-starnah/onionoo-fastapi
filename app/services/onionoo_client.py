from __future__ import annotations

import asyncio
import hashlib
import time
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

import httpx

from app.settings import settings


class UpstreamError(RuntimeError):
    def __init__(self, *, status_code: int, body: str | None):
        super().__init__(f"Onionoo upstream error: {status_code}")
        self.status_code = status_code
        self.body = body


@dataclass(frozen=True)
class UpstreamResponse:
    status_code: int
    headers: Mapping[str, str]
    json_body: Any | None
    text_body: str | None


def _clean_params(params: Mapping[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in params.items():
        if v is None:
            continue
        if isinstance(v, str) and v == "":
            continue
        out[k] = v
    return out


def _generate_cache_key(method: str, params: Mapping[str, Any], if_modified_since: str | None) -> str:
    """Generate a unique cache key for a request."""
    cache_data = {
        "method": method,
        "params": _clean_params(params),
        "if_modified_since": if_modified_since,
    }
    cache_str = str(sorted(cache_data.items()))
    return hashlib.sha256(cache_str.encode()).hexdigest()


class OnionooClient:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            base_url=settings.onionoo_base_url.rstrip("/"),
            timeout=httpx.Timeout(
                connect=10.0,  # Connection timeout
                read=30.0,     # Read timeout
                write=10.0,    # Write timeout
                pool=30.0      # Connection pool timeout
            ),
            limits=httpx.Limits(
                max_keepalive_connections=20,  # Keep-alive connections
                max_connections=100           # Maximum total connections
            ),
            headers={
                "Accept-Encoding": "gzip",
                "User-Agent": settings.user_agent,
            },
        )
        
        # Cache for storing responses with TTL
        self._cache: dict[str, tuple[UpstreamResponse, float]] = {}
        self._cache_ttl = 60.0  # 60 seconds TTL
        
        # Request deduplication for concurrent identical requests
        self._pending_requests: dict[str, asyncio.Future[UpstreamResponse]] = {}

    async def aclose(self) -> None:
        await self._client.aclose()

    async def get(
        self,
        *,
        method: str,
        params: Mapping[str, Any],
        if_modified_since: str | None,
    ) -> UpstreamResponse:
        # Generate cache key
        cache_key = _generate_cache_key(method, params, if_modified_since)
        
        # Check cache first
        current_time = time.time()
        if cache_key in self._cache:
            cached_response, timestamp = self._cache[cache_key]
            if current_time - timestamp < self._cache_ttl:
                return cached_response
            else:
                # Remove expired entry
                del self._cache[cache_key]
        
        # Check for in-flight identical requests (deduplication)
        if cache_key in self._pending_requests:
            return await self._pending_requests[cache_key]
        
        # Create new request
        url_path = f"/{method.lstrip('/')}"
        headers: dict[str, str] = {}
        if if_modified_since:
            headers["If-Modified-Since"] = if_modified_since

        # Create future for deduplication
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        self._pending_requests[cache_key] = future
        
        try:
            resp = await self._client.get(url_path, params=_clean_params(params), headers=headers)

            # 304 has no body.
            if resp.status_code == 304:
                response = UpstreamResponse(
                    status_code=resp.status_code,
                    headers=resp.headers,
                    json_body=None,
                    text_body=None,
                )
                # Cache 304 responses
                self._cache[cache_key] = (response, current_time)
                future.set_result(response)
                return response

            # Try to parse JSON; if it fails, keep text.
            json_body: Any | None = None
            text_body: str | None = None
            content_type = resp.headers.get("content-type", "")
            if "application/json" in content_type:
                try:
                    json_body = resp.json()
                except Exception:
                    text_body = resp.text
            else:
                text_body = resp.text

            if resp.status_code >= 400:
                error = UpstreamError(status_code=resp.status_code, body=text_body or None)
                future.set_exception(error)
                raise error

            response = UpstreamResponse(
                status_code=resp.status_code,
                headers=resp.headers,
                json_body=json_body,
                text_body=text_body,
            )
            
            # Cache successful responses
            self._cache[cache_key] = (response, current_time)
            future.set_result(response)
            return response
            
        except Exception as e:
            future.set_exception(e)
            raise
        finally:
            # Remove pending request
            self._pending_requests.pop(cache_key, None)
