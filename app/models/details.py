from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.models.envelope import OnionooEnvelope


class DetailsRelay(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    nickname: str
    fingerprint: str
    or_addresses: list[str]
    last_seen: str
    last_changed_address_or_port: str
    first_seen: str
    running: bool
    consensus_weight: int

    # Common optional fields (many more exist; extra fields are allowed)
    flags: list[str] | None = None
    country: str | None = None
    country_name: str | None = None
    as_number: str | None = Field(default=None, validation_alias="as", serialization_alias="as")
    as_name: str | None = None
    contact: str | None = None
    platform: str | None = None
    version: str | None = None
    recommended_version: bool | None = None
    version_status: str | None = None


class DetailsBridge(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    nickname: str
    hashed_fingerprint: str
    or_addresses: list[str]
    last_seen: str
    first_seen: str
    running: bool

    flags: list[str] | None = None
    platform: str | None = None
    version: str | None = None
    recommended_version: bool | None = None
    version_status: str | None = None
    contact: str | None = None


class DetailsResponse(OnionooEnvelope[DetailsRelay, DetailsBridge]):
    pass
