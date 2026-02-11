import asyncio
import logging

from typing import AsyncGenerator
from config import TEXT, DEFAULT_STREAMING_SPEED

from .base_provider import BaseProvider




logger = logging.getLogger(__name__)


class ProviderD(BaseProvider):

    """
    ProviderD simulates a stable inference provider with consistent latency and reliable streaming behavior.
    """

    async def stream(self) -> AsyncGenerator[str, None]:
        logger.info(f"Streaming From {self.__class__.__name__}")

        for chunk in TEXT.split():
            await asyncio.sleep(DEFAULT_STREAMING_SPEED)
            yield chunk

