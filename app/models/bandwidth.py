from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.models.envelope import OnionooEnvelope
from app.models.history import GraphHistory


class OverloadRateLimits(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    timestamp: int
    rate_limit: int = Field(validation_alias="rate-limit", serialization_alias="rate-limit")
    burst_limit: int = Field(validation_alias="burst-limit", serialization_alias="burst-limit")
    read_overload_count: int = Field(
        validation_alias="read-overload-count", serialization_alias="read-overload-count"
    )
    write_overload_count: int = Field(
        validation_alias="write-overload-count", serialization_alias="write-overload-count"
    )


class OverloadFdExhausted(BaseModel):
    model_config = ConfigDict(extra="allow")

    timestamp: int


class BandwidthRelay(BaseModel):
    model_config = ConfigDict(extra="allow")

    fingerprint: str
    write_history: dict[str, GraphHistory] | None = None
    read_history: dict[str, GraphHistory] | None = None
    overload_ratelimits: OverloadRateLimits | dict[str, Any] | None = None
    overload_fd_exhausted: OverloadFdExhausted | dict[str, Any] | None = None


class BandwidthBridge(BaseModel):
    """
    Upstream uses key name `fingerprint` but it's a SHA-1 hash of the bridge fingerprint.
    """

    model_config = ConfigDict(extra="allow")

    hashed_fingerprint: str = Field(validation_alias="fingerprint")
    write_history: dict[str, GraphHistory] | None = None
    read_history: dict[str, GraphHistory] | None = None
    overload_ratelimits: OverloadRateLimits | dict[str, Any] | None = None
    overload_fd_exhausted: OverloadFdExhausted | dict[str, Any] | None = None


class BandwidthResponse(OnionooEnvelope[BandwidthRelay, BandwidthBridge]):
    pass
