import config
import logging
import asyncio
from fastapi import FastAPI, Request
from starlette.responses import StreamingResponse
from orchestrator.orchestrator_service import OrchestratorService
from providers import ProviderManager


logger = logging.getLogger(__name__)
logger.info("********Application StreamOrchestrator started********")


app = FastAPI()
@app.get("/stream")
async def stream() -> StreamingResponse:
    orchestrator = OrchestratorService(ProviderManager)
    async def _generator():
        try:
            async for chunk in orchestrator.dynamic_provider_stream_handler():
                yield chunk
        except asyncio.CancelledError:
            logger.info("Client Disconnected")
            pass
    return StreamingResponse(_generator(), status_code=200, media_type="text/plain")
