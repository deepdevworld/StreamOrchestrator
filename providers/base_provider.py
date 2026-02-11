from abc import ABC, abstractmethod
from typing import AsyncGenerator




class BaseProvider(ABC):

    @abstractmethod
    def stream(self) -> AsyncGenerator[str, None]:
        """
            Stream the data
        """
        pass

