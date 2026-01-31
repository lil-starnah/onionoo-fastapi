from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.models.envelope import OnionooEnvelope
from app.models.history import GraphHistory
from app.models.misc import EmptyBridge


class WeightsRelay(BaseModel):
    model_config = ConfigDict(extra="allow")

    fingerprint: str = Field(
        description="Relay fingerprint (40 upper-case hexadecimal characters)."
    )

    consensus_weight_fraction: dict[str, GraphHistory] | None = Field(
        default=None,
        description=(
            "History of consensus_weight_fraction (path-selection probability approximation). "
            "Keys: 1_month, 6_months, 1_year, 5_years."
        ),
    )
    guard_probability: dict[str, GraphHistory] | None = Field(
        default=None,
        description=(
            "History of guard selection probability approximation. "
            "Keys: 1_month, 6_months, 1_year, 5_years."
        ),
    )
    middle_probability: dict[str, GraphHistory] | None = Field(
        default=None,
        description=(
            "History of middle selection probability approximation. "
            "Keys: 1_month, 6_months, 1_year, 5_years."
        ),
    )
    exit_probability: dict[str, GraphHistory] | None = Field(
        default=None,
        description=(
            "History of exit selection probability approximation. "
            "Keys: 1_month, 6_months, 1_year, 5_years."
        ),
    )
    consensus_weight: dict[str, GraphHistory] | None = Field(
        default=None,
        description=(
            "History of absolute consensus weight. Keys: 1_month, 6_months, 1_year, 5_years."
        ),
    )


class WeightsResponse(OnionooEnvelope[WeightsRelay, EmptyBridge]):
    pass
