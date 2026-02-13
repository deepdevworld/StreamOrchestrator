# StreamOrchestrator
A resilient streaming endpoint that dynamically switches between different providers based on set of criteria.


# RUN 
## Steps

Build server 
* open terminal inside the project directory.
* Run the following commands.
* Make sure port 8000 is free as the server is exposed to that port or else change it in the docker compose file as well as in curl command below.
* ```
  docker compose up --build -d
  ```
Tail the logs
* ```
  docker logs --tail 200 -f stream_orchestration
  ```

Run the client by opening the terminal.  
* If latency exception is not triggering then please run this command few time as random delay is generated.
* ```
  curl -N http://127.0.0.1:8000/stream
  ```

**To test what happens when provider is not available set `REGISTER_PROVIDER_FLAG=0` to disable the registration of the providers
and follow above steps again.**


## Providers
Providers simulate different inference services with varying performance characteristics such as latency, stability, and failure behavior.
* ### ProviderA,B,C,D: 
    Simulates interface provider with random failures.

## orchestrator
The OrchestratorService manages the streaming process and dynamically switches between
inference providers based on runtime performance metrics such as latency, timeouts, 
active_users_count and unavailability,
Providing smooth stream.



