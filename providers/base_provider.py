from abc import ABC, abstractmethod
from typing import AsyncGenerator

from health_metric.health_metric import HealthMetric


class BaseProvider(ABC):

    health_metric: HealthMetric

    @abstractmethod
    def stream(self) -> AsyncGenerator[str, None]:
        """
            Stream the data
        """
        pass

