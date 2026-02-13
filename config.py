import service_logging.logging_config

# This text will be streamed
TEXT="A resilient streaming endpoint that dynamically switches between different providers based on set of criteria."

# timeout for the providers to yield the response
STREAM_TIMEOUT=1

# base delay time for stream
DEFAULT_STREAMING_SPEED=0.2

# used for timeout trigger in ProviderA
MAX_STREAMING_DELAY=1.1

# latency delay will be randomly generates between  DEFAULT_STREAMING_SPEED - MAX_LATENCY_DELAY
MAX_LATENCY_DELAY=0.9

# max latency delay beyond which the latency exception will raise
OPERATIONAL_LATENCY_DELAY=0.7

# 1 to enable provider registration and 0 to disable provider registration.
REGISTER_PROVIDER_FLAG=1

FAILURE_COUNT_THRESHOLD=5

TIMEOUT_COUNT_THRESHOLD=3
# in sec
TIME_WINDOW=120

COOLDOWN_TIME=60

# weights
LATENCY_WEIGHT = 2
FAILURE_WEIGHT = 10
TIMEOUT_WEIGHT = 8
LOAD_WEIGHT = 1