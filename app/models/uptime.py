from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.models.envelope import OnionooEnvelope
from app.models.history import GraphHistory


class UptimeRelay(BaseModel):
    model_config = ConfigDict(extra="allow")

    fingerprint: str
    uptime: dict[str, GraphHistory] | None = None
    flags: dict[str, dict[str, GraphHistory]] | None = None


class UptimeBridge(BaseModel):
    """
    Upstream uses key name `fingerprint` but it's a SHA-1 hash of the bridge fingerprint.
    """

    model_config = ConfigDict(extra="allow")

    hashed_fingerprint: str = Field(validation_alias="fingerprint")
    uptime: dict[str, GraphHistory] | None = None


class UptimeResponse(OnionooEnvelope[UptimeRelay, UptimeBridge]):
    pass
