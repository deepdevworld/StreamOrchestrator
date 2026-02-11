import logging
import asyncio
import time
from typing import Type

from providers import ProviderManager
from exception_handlers.exception_handler import ProviderUnavailableError, TooManyActiveClientsError, LatencyError
from config import STREAM_TIMEOUT, OPERATIONAL_LATENCY_DELAY




logger = logging.getLogger(__name__)

class OrchestratorService:

    """
        The OrchestratorService manages the streaming process and dynamically switches between
        inference providers based on runtime performance metrics such as latency, timeouts,
        active_users_count and unavailability,
        Providing smooth stream.
    """

    def __init__(self, providers: Type[ProviderManager]):
        self.providers = providers.get_providers()
        self.streamed_chunk_count: int = 0
        self.streamed_chunk: str = ""
        self.skip_chunk: bool = False

    def _skip_chunk(self):
        if self.skip_chunk and self.streamed_chunk_count > 0:
            self.streamed_chunk_count -= 1
            return True
        self.skip_chunk = False
        return False



    async def dynamic_provider_stream_handler(self):
        for provider in self.providers:
            _provider = provider()
            _stream = _provider.stream()
            while True:
                try:
                    start_time = time.time()
                    chunk = await asyncio.wait_for(_stream.__anext__(), timeout=STREAM_TIMEOUT)

                    if self._skip_chunk():
                        continue

                    latency = time.time()-start_time
                    if latency > OPERATIONAL_LATENCY_DELAY:
                        raise LatencyError("Latency exceeded.")

                    self.streamed_chunk += f"{chunk} "
                    yield f"{chunk} "
                    self.streamed_chunk_count += 1

                except (ProviderUnavailableError, TooManyActiveClientsError, asyncio.TimeoutError, LatencyError) as e:
                    if isinstance(e, asyncio.TimeoutError):
                        e = "TimeoutError"
                    logger.warning(f"Switching Provider: {e} ")
                    logger.warning(f"Text streamed before switching: [{self.streamed_chunk}]")
                    self.skip_chunk = True
                    break
                except StopAsyncIteration:
                    return

        yield "Oops!! Service not available at the moment, Please try again later."