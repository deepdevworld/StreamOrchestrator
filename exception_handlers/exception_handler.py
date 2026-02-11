
class TooManyActiveClientsError(Exception):
    def __init__(self, count: int, message: str):
        self.count = count
        self.message = f"{self.__class__.__name__}: message: {message} count: {count}"
        super().__init__(self.message)


class ProviderUnavailableError(Exception):
    def __init__(self, message: str):
        self.message = f"{self.__class__.__name__}: {message}"
        super().__init__(self.message)


class LatencyError(Exception):
    def __init__(self, message: str):
        self.message = f"{self.__class__.__name__}: {message}"
        super().__init__(self.message)