from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.models.envelope import OnionooEnvelope
from app.models.history import GraphHistory


class OverloadRateLimits(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    timestamp: int = Field(description="Unix timestamp when overload rate limits were reported.")
    rate_limit: int = Field(
        validation_alias="rate-limit",
        serialization_alias="rate-limit",
        description="BandwidthRate value from torrc (bytes per second).",
    )
    burst_limit: int = Field(
        validation_alias="burst-limit",
        serialization_alias="burst-limit",
        description="BandwidthBurst value from torrc (bytes per second).",
    )
    read_overload_count: int = Field(
        validation_alias="read-overload-count",
        serialization_alias="read-overload-count",
        description="Count of times read burst/rate limits were exhausted.",
    )
    write_overload_count: int = Field(
        validation_alias="write-overload-count",
        serialization_alias="write-overload-count",
        description="Count of times write burst/rate limits were exhausted.",
    )


class OverloadFdExhausted(BaseModel):
    model_config = ConfigDict(extra="allow")

    timestamp: int = Field(description="Unix timestamp when FD exhaustion was reported.")


class BandwidthRelay(BaseModel):
    model_config = ConfigDict(extra="allow")

    fingerprint: str = Field(
        description="Relay fingerprint (40 upper-case hexadecimal characters)."
    )
    write_history: dict[str, GraphHistory] | None = Field(
        default=None,
        description="Written bytes per second history. Keys: 1_month, 6_months, 1_year, 5_years.",
    )
    read_history: dict[str, GraphHistory] | None = Field(
        default=None,
        description="Read bytes per second history. Keys: 1_month, 6_months, 1_year, 5_years.",
    )
    overload_ratelimits: OverloadRateLimits | dict[str, Any] | None = Field(
        default=None, description="Overload rate limit events (if any)."
    )
    overload_fd_exhausted: OverloadFdExhausted | dict[str, Any] | None = Field(
        default=None, description="File descriptor exhaustion events (if any)."
    )


class BandwidthBridge(BaseModel):
    """
    Upstream uses key name `fingerprint` but it's a SHA-1 hash of the bridge fingerprint.
    """

    model_config = ConfigDict(extra="allow")

    hashed_fingerprint: str = Field(
        validation_alias="fingerprint",
        description="SHA-1 hash of the bridge fingerprint (40 upper-case hexadecimal characters).",
    )
    write_history: dict[str, GraphHistory] | None = Field(
        default=None,
        description="Written bytes per second history. Keys: 1_month, 6_months, 1_year, 5_years.",
    )
    read_history: dict[str, GraphHistory] | None = Field(
        default=None,
        description="Read bytes per second history. Keys: 1_month, 6_months, 1_year, 5_years.",
    )
    overload_ratelimits: OverloadRateLimits | dict[str, Any] | None = Field(
        default=None, description="Overload rate limit events (if any)."
    )
    overload_fd_exhausted: OverloadFdExhausted | dict[str, Any] | None = Field(
        default=None, description="File descriptor exhaustion events (if any)."
    )


class BandwidthResponse(OnionooEnvelope[BandwidthRelay, BandwidthBridge]):
    pass
