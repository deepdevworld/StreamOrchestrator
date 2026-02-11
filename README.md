# StreamOrchestrator
A resilient streaming endpoint that dynamically switches between different providers based on set of criteria.


# RUN 
## steps

build server 
* ```
  docker compose up --build -d
  ```

Tail the logs
* ```
  docker logs --tail 200 -f stream_orchestrator
  ```

Run the client by opening the terminal.  
    **To test the ProviderC you need to run the command in two terminals.**  
    **If latency exception is not triggering then please run this command few time as random delay is generated.**
* ```
  curl -N http://127.0.0.1:8000/stream
  ```

**To test what happens when provider is not available set `REGISTER_PROVIDER_FLAG=0` to disable the registration of the providers
and follow above steps again.**


## Providers
Providers simulate different inference services with varying performance characteristics such as latency, stability, and failure behavior.
* ### ProviderA: 
    Simulates an unreliable inference provider with timeout failure.
* ### ProviderB: 
    Simulates an unavailable inference provider to test failure handling and fallback mechanisms.
* ### ProviderC: 
    Simulates an inference provider that enforces a maximum active client limit and
    rejects new streaming requests when the limit is exceeded.
* ### ProviderD: 
    Simulates a stable inference provider with consistent latency and reliable streaming behavior.
* ### ProviderE: 
    Simulates an unreliable inference provider with high latency and streaming speed.

## orchestrator
The OrchestratorService manages the streaming process and dynamically switches between
inference providers based on runtime performance metrics such as latency, timeouts, 
active_users_count and unavailability,
Providing smooth stream.



