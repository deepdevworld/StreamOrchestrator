import logging
import asyncio
import time
from typing import Type, Optional

from providers import ProviderManager
from exception_handlers.exception_handler import ProviderUnavailableError, TooManyActiveClientsError, LatencyError
from config import (STREAM_TIMEOUT, FAILURE_COUNT_THRESHOLD, TIMEOUT_COUNT_THRESHOLD, LATENCY_WEIGHT, TIMEOUT_WEIGHT,
                    FAILURE_WEIGHT, LOAD_WEIGHT)
from providers.base_provider import BaseProvider
from health_metric.health_metric import HealthMetricData

logger = logging.getLogger(__name__)

class OrchestratorService:

    """
        The OrchestratorService manages the streaming process and dynamically switches between
        inference providers based on runtime performance metrics such as latency, timeouts,
        active_users_count, cooldown_time and unavailability,
        Providing smooth stream.
    """

    def __init__(self, providers: Type[ProviderManager]):
        self.providers = providers.get_providers()
        self.streamed_chunk_count: int = 0
        self.streamed_chunk: str = ""
        self.skip_chunk: bool = False
        self.lock = asyncio.Lock()

    def _skip_chunk(self):
        if self.skip_chunk and self.streamed_chunk_count > 0:
            self.streamed_chunk_count -= 1
            return True
        self.skip_chunk = False
        return False

    def _is_healthy(self, health: HealthMetricData) -> bool:
        if health.is_in_cooldown:
            return False
        if health.failure_frequency > FAILURE_COUNT_THRESHOLD:
            return False
        if health.timeout_frequency > TIMEOUT_COUNT_THRESHOLD:
            return False
        return True

    async def _select_provider(self) -> Type[BaseProvider]:
        best_provider: Optional[Type[BaseProvider]] = None
        current_metric = None
        for provider in self.providers:
            health_metric_data = await provider.health_metric.get_health_metric_data()

            if not self._is_healthy(health_metric_data):
                logger.warning(f"setting provider: {provider.__name__} for cooldown")
                await provider.health_metric.set_cooldown()
                continue

            health_metric = (health_metric_data.response_time * LATENCY_WEIGHT,
                             health_metric_data.failure_frequency * FAILURE_WEIGHT,
                             health_metric_data.timeout_frequency * TIMEOUT_WEIGHT,
                             health_metric_data.active_clients * LOAD_WEIGHT
                             )

            if best_provider is None:
                best_provider = provider
                current_metric = health_metric

            elif current_metric > health_metric:
                best_provider = provider
                current_metric = health_metric

        if best_provider is None:
            raise ProviderUnavailableError("Oops!! Provider not available")

        return best_provider


    async def dynamic_provider_stream_handler(self):
        while True:
            try:
                provider_cls = await self._select_provider()
                provider = provider_cls()
                stream = provider.stream()
                chunks_to_skip = self.streamed_chunk_count

                while True:
                    try:
                        start_time = time.time()
                        chunk = await asyncio.wait_for(stream.__anext__(), timeout=STREAM_TIMEOUT)
                        response_time = time.time()-start_time

                        await provider.health_metric.add_response_time(response_time)
                        if chunks_to_skip > 0:
                            chunks_to_skip -= 1
                            continue

                        self.streamed_chunk += f"{chunk} "
                        yield f"{chunk} "
                        self.streamed_chunk_count += 1

                    except (ProviderUnavailableError, TooManyActiveClientsError, asyncio.TimeoutError, LatencyError) as e:
                        if isinstance(e, asyncio.TimeoutError):
                            e = "TimeoutError"
                            await provider.health_metric.add_timeout()
                        if isinstance(e, ProviderUnavailableError):
                            await provider.health_metric.add_failure()

                        logger.warning(f"Switching Provider: {e} ")
                        logger.warning(f"Text streamed before switching: [{self.streamed_chunk}]")
                        break
                    except StopAsyncIteration:
                        return
            except ProviderUnavailableError as e:
                logger.error(f"Provider Unavailable: {e}")
                break
        yield "Oops!! Service not available at the moment, Please try again later."
