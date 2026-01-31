from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.models.envelope import OnionooEnvelope
from app.models.history import GraphHistory
from app.models.misc import EmptyRelay


class ClientsBridge(BaseModel):
    """
    Upstream uses key name `fingerprint` but it's a SHA-1 hash of the bridge fingerprint.
    """

    model_config = ConfigDict(extra="allow")

    hashed_fingerprint: str = Field(
        validation_alias="fingerprint",
        description="SHA-1 hash of the bridge fingerprint (40 upper-case hexadecimal characters).",
    )
    average_clients: dict[str, GraphHistory] | None = Field(
        default=None,
        description=(
            "History of estimated average number of clients per day. "
            "Keys: 1_month, 6_months, 1_year, 5_years."
        ),
    )


class ClientsResponse(OnionooEnvelope[EmptyRelay, ClientsBridge]):
    pass
