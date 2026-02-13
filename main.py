import config
import logging
import asyncio
from fastapi import FastAPI, Request
from starlette.responses import StreamingResponse

from exception_handlers.exception_handler import ProviderUnavailableError
from orchestrator.orchestrator_service import OrchestratorService
from providers import ProviderManager, ProviderA, ProviderB, ProviderC, ProviderD
from contextlib import asynccontextmanager


logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("********Application StreamOrchestrator started********")
    # registering the providers

    if config.REGISTER_PROVIDER_FLAG:
        ProviderManager.register(ProviderA)
        ProviderManager.register(ProviderB)
        ProviderManager.register(ProviderC)
        ProviderManager.register(ProviderD)

    yield
    logger.info("********Application StreamOrchestrator stopped********")

app = FastAPI(lifespan=lifespan)
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
        except ProviderUnavailableError as e:
            logger.info("ProviderUnavailableError")
            pass
        finally:
            # to print new line in terminal after the text is streamed
            yield "\n"
    return StreamingResponse(_generator(), status_code=200, media_type="text/plain")
