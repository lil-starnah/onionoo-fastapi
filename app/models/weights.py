from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from app.models.envelope import OnionooEnvelope
from app.models.history import GraphHistory
from app.models.misc import EmptyBridge


class WeightsRelay(BaseModel):
    model_config = ConfigDict(extra="allow")

    fingerprint: str

    consensus_weight_fraction: dict[str, GraphHistory] | None = None
    guard_probability: dict[str, GraphHistory] | None = None
    middle_probability: dict[str, GraphHistory] | None = None
    exit_probability: dict[str, GraphHistory] | None = None
    consensus_weight: dict[str, GraphHistory] | None = None


class WeightsResponse(OnionooEnvelope[WeightsRelay, EmptyBridge]):
    pass
