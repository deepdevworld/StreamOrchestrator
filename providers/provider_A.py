import logging
import asyncio
import random

from typing import AsyncGenerator
from config import TEXT, MAX_STREAMING_DELAY

from .base_provider import BaseProvider




logger = logging.getLogger(__name__)


class ProviderA(BaseProvider):

    """
    Simulates an unreliable inference provider with timeout failure.
    """

    async def stream(self) -> AsyncGenerator[str, None]:
        logger.info(f"Streaming From {self.__class__.__name__}")

        for chunk in TEXT.split():
            await asyncio.sleep(MAX_STREAMING_DELAY)
            yield chunk
