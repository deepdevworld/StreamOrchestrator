import logging
import asyncio

from typing import AsyncGenerator
from config import TEXT, DEFAULT_STREAMING_SPEED, PROVIDER_C_MAX_CLIENT

from .base_provider import BaseProvider
from exception_handlers.exception_handler import TooManyActiveClientsError




logger = logging.getLogger(__name__)


class ProviderC(BaseProvider):

    """
    Simulates an inference provider that enforces a maximum active client limit and
    rejects new streaming requests when the limit is exceeded.
    """

    active_client_count = 0

    async def stream(self) -> AsyncGenerator[str, None]:
        try:
            ProviderC.active_client_count += 1
            logger.info(f"Streaming From  {self.__class__.__name__}, {self.__class__.active_client_count} active clients")

            for chunk in TEXT.split():
                if ProviderC.active_client_count > PROVIDER_C_MAX_CLIENT:
                    raise TooManyActiveClientsError(count=ProviderC.active_client_count, message=ProviderC.__name__)
                else:
                    await asyncio.sleep(DEFAULT_STREAMING_SPEED)
                yield chunk
        finally:
            ProviderC.active_client_count -= 1