from config import REGISTER_PROVIDER_FLAG
from .provider_manager import ProviderManager
from .provider_A import ProviderA
from .provider_B import ProviderB
from .provider_C import ProviderC
from .provider_D import ProviderD
from .provider_E import ProviderE

# registering the providers
if REGISTER_PROVIDER_FLAG:
    ProviderManager.register(ProviderA)
    ProviderManager.register(ProviderE)
    ProviderManager.register(ProviderB)
    ProviderManager.register(ProviderC)
    ProviderManager.register(ProviderD)
