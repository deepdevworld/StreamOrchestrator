from dataclasses import dataclass
import asyncio
import time
from collections import deque

from config import TIME_WINDOW, COOLDOWN_TIME


@dataclass
class HealthMetricData:
    response_time: float
    failure_frequency: int
    timeout_frequency: int
    is_in_cooldown: bool
    active_clients: int

class HealthMetric:
    def __init__(self):
        self.response_times: deque = deque(maxlen=5)
        self.total_failure_count: int = 0
        self.failure_timestamp: deque = deque(maxlen=1000)
        self.total_timeout_count: int = 0
        self.timeout_timestamp: deque = deque(maxlen=1000)
        self.cooldown_time: float = 0.0
        self.active_clients: int = 0
        self.__lock = asyncio.Lock()


    def get_response_time(self):
        if not self.response_times:
            return 0.0
        return sum(self.response_times)/len(self.response_times)

    async def add_response_time(self, response_time: float):
        async with self.__lock:
            self.response_times.append(response_time)

    async def add_failure(self):
        async with self.__lock:
            self.total_failure_count += 1
            self.failure_timestamp.append(time.time())

    async def failure_frequency(self):
        async with self.__lock:
            min_ago = time.time() - TIME_WINDOW
            while self.failure_timestamp and self.failure_timestamp[0] < min_ago:
                self.failure_timestamp.popleft()
            return len(self.failure_timestamp)

    async def add_timeout(self):
        async with self.__lock:
            self.total_timeout_count += 1
            self.timeout_timestamp.append(time.time())

    async def timeout_frequency(self):
        async with self.__lock:
            min_ago = time.time() - TIME_WINDOW
            while self.timeout_timestamp and self.timeout_timestamp[0] < min_ago:
                self.timeout_timestamp.popleft()
            return len(self.timeout_timestamp)

    async def set_cooldown(self):
        async with self.__lock:
            self.cooldown_time = time.time() + COOLDOWN_TIME

    def is_in_cooldown(self) -> bool:
        return time.time() < self.cooldown_time

    async def add_active_clients(self):
        async with self.__lock:
            self.active_clients += 1

    async def remove_active_clients(self):
        async with self.__lock:
            self.active_clients -= 1

    async def get_health_metric_data(self) -> HealthMetricData:
        _response_time = self.get_response_time()
        _failure_frequency = await self.failure_frequency()
        _timeout_frequency = await self.timeout_frequency()
        _is_in_cooldown = self.is_in_cooldown()
        return HealthMetricData(response_time=_response_time,
                                failure_frequency=_failure_frequency,
                                timeout_frequency=_timeout_frequency,
                                is_in_cooldown=_is_in_cooldown,
                                active_clients=self.active_clients
                                )
