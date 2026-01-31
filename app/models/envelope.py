from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

RelayT = TypeVar("RelayT")
BridgeT = TypeVar("BridgeT")


class OnionooEnvelope(BaseModel, Generic[RelayT, BridgeT]):
    """
    Onionoo responses share a common envelope across all methods.

    Spec: https://metrics.torproject.org/onionoo.html
    """

    model_config = ConfigDict(extra="allow")

    version: str
    next_major_version_scheduled: str | None = None
    build_revision: str | None = None

    relays_published: str
    relays_skipped: int | None = None
    relays_truncated: int | None = None
    relays: list[RelayT] = Field(default_factory=list)

    bridges_published: str
    bridges_skipped: int | None = None
    bridges_truncated: int | None = None
    bridges: list[BridgeT] = Field(default_factory=list)
