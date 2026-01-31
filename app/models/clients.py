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

    hashed_fingerprint: str = Field(validation_alias="fingerprint")
    average_clients: dict[str, GraphHistory] | None = None


class ClientsResponse(OnionooEnvelope[EmptyRelay, ClientsBridge]):
    pass
