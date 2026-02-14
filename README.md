# onionoo-fastapi

FastAPI-based **semantic/OpenAPI proxy** for the Tor **Onionoo** API.

- GitHub: <https://github.com/anoni-net/onionoo-fastapi>
- Upstream data source: <https://onionoo.torproject.org>
- This service **does not store Onionoo data**, it only forwards requests and transforms responses.
- Primary motivation: Onionoo has a solid spec, but **no OpenAPI**; this service provides a friendly schema **for tooling/AI agents**.

Reference spec: [Tor Metrics – Onionoo](https://metrics.torproject.org/onionoo.html)

## Hosted instance

- Service: `https://onionoo.anoni.net`
- Swagger UI: `https://onionoo.anoni.net/docs`

## License

MIT. See `LICENSE`.

## Requirements

- Python 3.12+
- [`uv`](https://docs.astral.sh/uv/) (for Cloudflare Workers: uv 0.8.10+)

## Install

```bash
git clone https://github.com/anoni-net/onionoo-fastapi
cd onionoo-fastapi
uv sync
```

For running the server locally (uvicorn) or with Docker, add the server extra:

```bash
uv sync --extra server
```

## Run

```bash
uv sync --extra server
fastapi run app.main:app --reload --host 0.0.0.0 --port 8000
```
**Note:** `fastapi run` requires FastAPI 0.110+ and the `server` extra (uvicorn).

OpenAPI docs:

- Swagger UI: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## Test

```bash
uv sync --extra dev
uv run pytest
```

## Deploy to Cloudflare Workers

This app can run on [Cloudflare Workers](https://workers.cloudflare.com/) (Python Workers, open beta). Same codebase as uvicorn/Docker; the Worker entrypoint is `worker.py`.

**Setup**

- Install the Workers CLI: `uv tool install workers-py` (requires Node.js and uv 0.8.10+).
- Ensure `wrangler.toml` exists (see repo); run `uv run pywrangler init` if you need to regenerate it.

**Configuration**

- Set env in `wrangler.toml` under `[vars]` (e.g. `ONIONOO_BASE_URL`, `DEFAULT_LIMIT`, `MAX_LIMIT`) or via [Secrets](https://developers.cloudflare.com/workers/configuration/secrets/) in the dashboard.
- The app reads config from the environment (Workers inject vars/secrets into the runtime).

**Local**

```bash
uv sync --extra dev
uv run pywrangler dev
```

**Deploy**

```bash
uv run pywrangler deploy
```

Python Workers are in **open beta** and require the `python_workers` (and optionally `python_dedicated_snapshot`) compatibility flags in `wrangler.toml`.

**Note (local dev):** When running `pywrangler dev`, the second request to the same or another endpoint can be much slower than the first (tens of seconds). This is due to the Workers/Pyodide runtime: the next request is not processed until the previous response has finished being sent. Deployed Workers on Cloudflare’s edge do not show this behavior.

## Docker

Build and run with Docker Compose:

```bash
docker compose up -d --build
```

If port 8000 is already in use, override host port (example: 8001):

```bash
HOST_PORT=8001 docker compose up -d --build
```

Stop:

```bash
docker compose down
```

Configuration via environment variables (example):

```bash
ONIONOO_BASE_URL=https://onionoo.torproject.org HOST_PORT=8001 docker compose up -d --build
```

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
- `ONIONOO_TIMEOUT_SECONDS` (default: `30`)
- `DEFAULT_LIMIT` (default: `100`)
- `MAX_LIMIT` (default: `200`)
- `USER_AGENT`

