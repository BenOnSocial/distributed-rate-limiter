# Distributed Rate Limiter (Redis + Lua)

A high-concurrency rate-limiting engine designed for distributed systems. This service enforces per-IP request limits using an **atomic sliding window algorithm**, ensuring consistency across 500+ service nodes without the latency overhead of global locks.

## 🚀 Architectural Decisions
- **Lua Atomicity:** Logic (Evict -> Count -> Add) is encapsulated in a server-side Lua script. This reduces network round-trips to a single call and guarantees atomicity, preventing race conditions during concurrent requests.
- **Sorted Set (ZSET) Storage:** Uses Redis Sorted Sets (`ZSET`) with timestamps as scores. This allows O(log N) eviction of expired requests, keeping the system performant even under heavy load.
- **Dependency Injection:** The `timestamp` is passed as a parameter, enabling deterministic unit testing of the sliding window without time-dependent flakiness.

## 🚀 Getting Started
1. Start the Docker Compose cluster:
   ```bash
   docker-compose up --build
   ```
2. The `app` container will automatically run the `app.py` test loop, demonstrating the 5-request limit enforcement.

## 🧠 Why this scales
By partitioning state by IP address and using server-side Lua, this engine eliminates the "global bottleneck" problem. Each IP is processed in isolation, allowing for massive horizontal scaling across any number of application nodes.
