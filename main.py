import config
import logging
import asyncio
from fastapi import FastAPI, Request
from starlette.responses import StreamingResponse
from orchestrator.orchestrator_service import OrchestratorService
from providers import ProviderManager
from contextlib import asynccontextmanager


logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("********Application StreamOrchestrator started********")
    yield
    logger.info("********Application StreamOrchestrator stopped********")

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
        finally:
            # to print new line in terminal after the text is streamed
            yield "\n"
    return StreamingResponse(_generator(), status_code=200, media_type="text/plain")
