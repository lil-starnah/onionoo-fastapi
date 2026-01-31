from pydantic import BaseModel, ConfigDict


class EmptyRelay(BaseModel):
    """Used for endpoints that don't contain relay objects (e.g. /clients)."""

    model_config = ConfigDict(extra="allow")


class EmptyBridge(BaseModel):
    """Used for endpoints that don't contain bridge objects (e.g. /weights)."""

    model_config = ConfigDict(extra="allow")
