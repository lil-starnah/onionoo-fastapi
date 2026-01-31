from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.models.envelope import OnionooEnvelope
from app.models.history import GraphHistory


class UptimeRelay(BaseModel):
    model_config = ConfigDict(extra="allow")

    fingerprint: str = Field(
        description="Relay fingerprint (40 upper-case hexadecimal characters)."
    )
    uptime: dict[str, GraphHistory] | None = Field(
        default=None,
        description=(
            "History of fractional uptime (0..1). Keys: 1_month, 6_months, 1_year, 5_years."
        ),
    )
    flags: dict[str, dict[str, GraphHistory]] | None = Field(
        default=None,
        description=(
            "Per-flag fractional times assigned. Outer keys: flag names (e.g. 'Running', 'Exit'). "
            "Inner keys: time ranges."
        ),
    )


class UptimeBridge(BaseModel):
    """
    Upstream uses key name `fingerprint` but it's a SHA-1 hash of the bridge fingerprint.
    """

    model_config = ConfigDict(extra="allow")

    hashed_fingerprint: str = Field(
        validation_alias="fingerprint",
        description="SHA-1 hash of the bridge fingerprint (40 upper-case hexadecimal characters).",
    )
    uptime: dict[str, GraphHistory] | None = Field(
        default=None,
        description=(
            "History of fractional uptime (0..1). Keys: 1_month, 6_months, 1_year, 5_years."
        ),
    )


class UptimeResponse(OnionooEnvelope[UptimeRelay, UptimeBridge]):
    pass
