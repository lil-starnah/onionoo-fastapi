from __future__ import annotations

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


class OnionooClient:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            base_url=settings.onionoo_base_url.rstrip("/"),
            timeout=httpx.Timeout(settings.onionoo_timeout_seconds),
            headers={
                "Accept-Encoding": "gzip",
                "User-Agent": settings.user_agent,
            },
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    async def get(
        self,
        *,
        method: str,
        params: Mapping[str, Any],
        if_modified_since: str | None,
    ) -> UpstreamResponse:
        url_path = f"/{method.lstrip('/')}"
        headers: dict[str, str] = {}
        if if_modified_since:
            headers["If-Modified-Since"] = if_modified_since

        resp = await self._client.get(url_path, params=_clean_params(params), headers=headers)

        # 304 has no body.
        if resp.status_code == 304:
            return UpstreamResponse(
                status_code=resp.status_code,
                headers=resp.headers,
                json_body=None,
                text_body=None,
            )

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
            raise UpstreamError(status_code=resp.status_code, body=text_body or None)

        return UpstreamResponse(
            status_code=resp.status_code,
            headers=resp.headers,
            json_body=json_body,
            text_body=text_body,
        )
