import asyncio
import logging
import random

from typing import AsyncGenerator
from health_metric.health_metric import HealthMetric
from config import TEXT, DEFAULT_STREAMING_SPEED, MAX_STREAMING_DELAY
from exception_handlers.exception_handler import ProviderUnavailableError

from .base_provider import BaseProvider

logger = logging.getLogger(__name__)


class ProviderD(BaseProvider):

    """
    Simulates streaming provider with random failures.
    """

    health_metric: HealthMetric = HealthMetric()

    async def stream(self) -> AsyncGenerator[str, None]:
        try:
            await self.health_metric.add_active_clients()
            logger.info(f"Streaming From {self.__class__.__name__}")
            for chunk in TEXT.split():
                # random delay for latency
                await asyncio.sleep(DEFAULT_STREAMING_SPEED)
                if random.random() > 0.9:
                    await asyncio.sleep(random.uniform(DEFAULT_STREAMING_SPEED, MAX_STREAMING_DELAY))
                # random failure of the provider
                if random.random() > 0.9:
                    raise ProviderUnavailableError(self.__class__.__name__)
                yield chunk
        finally:
            await self.health_metric.remove_active_clients()