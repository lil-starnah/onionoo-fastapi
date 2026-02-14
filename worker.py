"""Cloudflare Workers entrypoint: runs the FastAPI app via ASGI."""
from workers import WorkerEntrypoint

from app.main import create_app

app = create_app()


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        import asgi

        return await asgi.fetch(app, request.js_object, self.env)
