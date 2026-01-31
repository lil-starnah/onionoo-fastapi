from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.models.envelope import OnionooEnvelope


class SummaryRelay(BaseModel):
    """
    Semantic relay summary.

    Upstream uses short keys: n, f, a, r.
    """

    model_config = ConfigDict(extra="allow")

    nickname: str = Field(
        validation_alias="n",
        description="Relay nickname (1–19 alphanumerical characters).",
    )
    fingerprint: str = Field(
        validation_alias="f",
        description="Relay fingerprint (40 upper-case hexadecimal characters).",
    )
    addresses: list[str] = Field(
        validation_alias="a",
        description=(
            "IPv4/IPv6 addresses where the relay accepts onion-routing connections (or used to exit "
            "in the past 24 hours)."
        ),
    )
    running: bool = Field(
        validation_alias="r",
        description="Whether this relay was listed as Running in the last consensus.",
    )


class SummaryBridge(BaseModel):
    """
    Semantic bridge summary.

    Upstream uses short keys: n, h, r.
    """

    model_config = ConfigDict(extra="allow")

    nickname: str = Field(
        validation_alias="n",
        description="Bridge nickname (1–19 alphanumerical characters).",
    )
    hashed_fingerprint: str = Field(
        validation_alias="h",
        description="SHA-1 hash of the bridge fingerprint (40 upper-case hexadecimal characters).",
    )
    running: bool = Field(
        validation_alias="r",
        description="Whether this bridge was successfully tested (or listed as running if untested).",
    )


class SummaryResponse(OnionooEnvelope[SummaryRelay, SummaryBridge]):
    pass
