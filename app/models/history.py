from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class GraphHistory(BaseModel):
    """
    Graph history objects used across Onionoo documents.
    """

    model_config = ConfigDict(extra="allow")

    first: str
    last: str
    interval: int
    factor: float
    count: int | None = None
    values: list[int | None]
