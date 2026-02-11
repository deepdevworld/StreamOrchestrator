import logging
import asyncio
import random

from typing import AsyncGenerator
from config import TEXT, DEFAULT_STREAMING_SPEED, MAX_LATENCY_DELAY

from .base_provider import BaseProvider




logger = logging.getLogger(__name__)


class ProviderE(BaseProvider):

    """
    Simulates an unreliable inference provider with high latency and streaming speed.
    """

    async def stream(self) -> AsyncGenerator[str, None]:
        logger.info(f"Streaming From {self.__class__.__name__}")

        for chunk in TEXT.split():
            await asyncio.sleep(random.uniform(DEFAULT_STREAMING_SPEED, MAX_LATENCY_DELAY))
            yield chunk