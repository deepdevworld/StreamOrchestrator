from typing import List, Type
from .base_provider import BaseProvider




class ProviderManager:
    """
        ProviderManager holds the list of providers.
    """

    _providers: List[Type[BaseProvider]] = list()

    @classmethod
    def register(cls, provider: Type[BaseProvider]):
        if provider not in cls._providers:
            cls._providers.append(provider)

    @classmethod
    def get_providers(cls) -> List[Type[BaseProvider]]:
        return cls._providers

