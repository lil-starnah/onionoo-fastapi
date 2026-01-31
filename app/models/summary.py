from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.models.envelope import OnionooEnvelope


class SummaryRelay(BaseModel):
    """
    Semantic relay summary.

    Upstream uses short keys: n, f, a, r.
    """

    model_config = ConfigDict(extra="allow")

    nickname: str = Field(validation_alias="n")
    fingerprint: str = Field(validation_alias="f")
    addresses: list[str] = Field(validation_alias="a")
    running: bool = Field(validation_alias="r")


class SummaryBridge(BaseModel):
    """
    Semantic bridge summary.

    Upstream uses short keys: n, h, r.
    """

    model_config = ConfigDict(extra="allow")

    nickname: str = Field(validation_alias="n")
    hashed_fingerprint: str = Field(validation_alias="h")
    running: bool = Field(validation_alias="r")


class SummaryResponse(OnionooEnvelope[SummaryRelay, SummaryBridge]):
    pass
