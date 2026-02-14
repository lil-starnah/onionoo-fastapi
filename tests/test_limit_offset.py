"""Test that limit and offset parameters work correctly."""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Use context manager so ASGI app is run correctly."""
    with TestClient(app) as c:
        yield c


def test_limit_returns_requested_count(client: TestClient) -> None:
    """limit=N should return N relays."""
    r = client.get("/v1/summary", params={"type": "relay", "limit": 5})
    r.raise_for_status()
    data = r.json()
    relays = data.get("relays", [])
    assert len(relays) == 5, f"Expected 5 relays, got {len(relays)}"


def test_offset_skips_relays(client: TestClient) -> None:
    """offset=N should return relays starting after the first N."""
    r1 = client.get("/v1/summary", params={"type": "relay", "limit": 5})
    r1.raise_for_status()
    relays1 = r1.json().get("relays", [])

    r2 = client.get(
        "/v1/summary", params={"type": "relay", "limit": 5, "offset": 5}
    )
    r2.raise_for_status()
    relays2 = r2.json().get("relays", [])

    fp1 = relays1[0].get("fingerprint") or relays1[0].get("f")
    fp2 = relays2[0].get("fingerprint") or relays2[0].get("f")
    assert fp1 != fp2, f"offset should skip relays; both batches started with {fp1}"


def test_offset_matches_slice_of_full_fetch(client: TestClient) -> None:
    """offset=5 batch should match indices 5-9 of a limit=10 fetch."""
    r_full = client.get(
        "/v1/summary", params={"type": "relay", "limit": 10, "offset": 0}
    )
    r_full.raise_for_status()
    full_relays = r_full.json().get("relays", [])

    r_offset = client.get(
        "/v1/summary", params={"type": "relay", "limit": 5, "offset": 5}
    )
    r_offset.raise_for_status()
    offset_relays = r_offset.json().get("relays", [])

    expected_fps = [
        r.get("fingerprint") or r.get("f") for r in full_relays[5:10]
    ]
    actual_fps = [
        r.get("fingerprint") or r.get("f") for r in offset_relays
    ]
    assert expected_fps == actual_fps, (
        f"offset=5 batch should match indices 5-9 of full fetch. "
        f"Expected {expected_fps}, got {actual_fps}"
    )
