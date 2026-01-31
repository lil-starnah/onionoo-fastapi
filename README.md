# onionoo-fastapi

FastAPI-based **semantic/OpenAPI proxy** for the Tor **Onionoo** API.

- Upstream data source: <https://onionoo.torproject.org>
- This service **does not store Onionoo data**, it only forwards requests and transforms responses.
- Primary motivation: Onionoo has a solid spec, but **no OpenAPI**; this service provides a friendly schema **for tooling/AI agents**.

Reference spec: [Tor Metrics – Onionoo](https://metrics.torproject.org/onionoo.html)

## License

MIT. See `LICENSE`.

## Requirements

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/)

## Install

```bash
cd onionoo-fastapi
uv sync
```

## Run

```bash
fastapi run app.main:app --reload --host 0.0.0.0 --port 8000
```
**Note:** `fastapi run` requires FastAPI version 0.110.0 or newer.

OpenAPI docs:

- Swagger UI: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## API

This service exposes semantic endpoints under `/v1/*`:

- `GET /v1/summary`
- `GET /v1/details`
- `GET /v1/bandwidth`
- `GET /v1/weights`
- `GET /v1/clients`
- `GET /v1/uptime`

Plus:

- `GET /healthz`

### Example requests

```bash
# Summary (semantic keys; upstream short keys are transformed)
curl -s 'http://localhost:8000/v1/summary?limit=1' | jq .

# Details (supports Onionoo query parameters + details-only `fields`)
curl -s 'http://localhost:8000/v1/details?limit=1&search=moria&fields=nickname,fingerprint' | jq .

# Bandwidth
curl -s 'http://localhost:8000/v1/bandwidth?limit=1&search=moria' | jq .

# Weights (relays only)
curl -s 'http://localhost:8000/v1/weights?limit=1&search=moria' | jq .

# Clients (bridges only)
curl -s 'http://localhost:8000/v1/clients?limit=1' | jq .

# Uptime
curl -s 'http://localhost:8000/v1/uptime?limit=1&search=moria' | jq .
```

### Semantic field mapping notes

- `/v1/summary` transforms Onionoo short keys:
  - relay: `n,f,a,r` → `nickname,fingerprint,addresses,running`
  - bridge: `n,h,r` → `nickname,hashed_fingerprint,running`
- For some bridge documents (`/bandwidth`, `/clients`, `/uptime`), Onionoo uses the key name `fingerprint` even though the value is a **hashed fingerprint**; this API exposes that as `hashed_fingerprint`.

### Caching / 304 behavior

If the client includes `If-Modified-Since`, it will be forwarded upstream. If Onionoo replies with `304`, this service will reply `304` too.

### Configuration

- `ONIONOO_BASE_URL` (default: `https://onionoo.torproject.org`)

