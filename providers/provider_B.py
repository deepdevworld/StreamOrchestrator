from typing import AsyncGenerator
from .base_provider import BaseProvider
from exception_handlers.exception_handler import ProviderUnavailableError
import logging
import asyncio
from config import DEFAULT_STREAMING_SPEED




logger = logging.getLogger(__name__)


class ProviderB(BaseProvider):

    """
    Simulates an unavailable inference provider to test failure handling and fallback mechanisms.
    """

    async def stream(self) -> AsyncGenerator[str, None]:
        logger.info(f"Streaming From {self.__class__.__name__}")

        await asyncio.sleep(DEFAULT_STREAMING_SPEED)
        raise ProviderUnavailableError(ProviderB.__name__)
        yield ""
