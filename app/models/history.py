from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class GraphHistory(BaseModel):
    """
    Graph history objects used across Onionoo documents.
    """

    model_config = ConfigDict(extra="allow")

    first: str = Field(
        description=(
            "UTC timestamp (YYYY-MM-DD hh:mm:ss) of the first data point "
            "(more precisely: interval midpoint of the first interval)."
        )
    )
    last: str = Field(
        description=(
            "UTC timestamp (YYYY-MM-DD hh:mm:ss) of the last data point "
            "(more precisely: interval midpoint of the last interval)."
        )
    )
    interval: int = Field(description="Time interval between two data points, in seconds.")
    factor: float = Field(
        description=(
            "Factor by which normalized values must be multiplied to obtain original values."
        )
    )
    count: int | None = Field(
        default=None,
        description="Number of values (optional; can be derived from the values array length).",
    )
    values: list[int | None] = Field(
        description="Array of normalized values (0..999) or nulls. Multiply by factor for original."
    )
