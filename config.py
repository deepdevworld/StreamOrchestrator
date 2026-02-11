import os
from dotenv import load_dotenv
import service_logging.logging_config

load_dotenv()
DEFAULT_STREAMING_SPEED = float(os.getenv("DEFAULT_STREAMING_SPEED"))
TEXT = str(os.getenv("TEXT"))
PROVIDER_C_MAX_CLIENT = int(os.getenv("PROVIDER_C_MAX_CLIENT"))
MAX_STREAMING_DELAY = float(os.getenv("MAX_STREAMING_DELAY"))
MAX_LATENCY_DELAY = float(os.getenv("MAX_LATENCY_DELAY"))
OPERATIONAL_LATENCY_DELAY = float(os.getenv("OPERATIONAL_LATENCY_DELAY"))
STREAM_TIMEOUT = float(os.getenv("STREAM_TIMEOUT"))
REGISTER_PROVIDER_FLAG = bool(os.getenv("REGISTER_PROVIDER_FLAG") == '1')