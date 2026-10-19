# Chaos Kitchen — Project Report

## Overview

Chaos Kitchen is a beginner-friendly chaos engineering project built with Python and FastAPI. The goal is to simulate real-world application failures in a controlled local environment and observe how the system responds. It uses a simple food-ordering API as the target application, introduces failures through chaos experiments, and measures system behaviour through a monitoring layer.

---

## Project Structure

```
chaos-kitchen/
├── app/                  # Food-ordering API
│   ├── main.py           # FastAPI app, routes, middleware
│   ├── orders.py         # Order storage and retrieval logic
│   ├── database.py       # Database access layer
│   ├── metrics.py        # Metrics recording bridge
│   └── __init__.py
├── chaos/                # Chaos experiment modules
│   ├── runner.py         # Experiment dispatcher
│   ├── slow_database.py  # Simulates database latency
│   ├── break_dns.py      # Simulates DNS failure
│   ├── kill_services.py  # Simulates service termination
│   └── __init__.py
├── monitor/              # Observability layer
│   ├── collector.py      # Metrics collection and storage
│   ├── dashboard.py      # Metrics retrieval for display
│   └── __init__.py
├── test/                 # Automated test suites
│   ├── test_orders.py
│   ├── test_chaos.py
│   ├── test_monitor.py
│   └── test_resilience.py
├── Dockerfile
├── compose.yaml
└── requirements.txt
```

---

## What Was Built

### 1. Food-Ordering API (`app/`)

The core application is a REST API with the following endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/orders` | Place a new order |
| GET | `/orders` | List all orders |
| GET | `/orders/{id}` | Fetch a specific order by ID |
| GET | `/health` | Check application health |

Key implementation details:
- Built with **FastAPI** and **Pydantic** for request validation
- Orders are stored in an in-memory dictionary with auto-incrementing IDs
- A `database.get_db()` abstraction layer wraps data access, making it mockable in tests
- All database-dependent routes catch exceptions and return `503 Service Unavailable` instead of crashing
- The `/health` endpoint reports `{"status": "ok"}` normally, and `{"status": "degraded", "db": "down"}` when the database is unreachable
- An HTTP middleware layer automatically records every request's route, status code, and response time to the monitor

### 2. Chaos Experiments (`chaos/`)

Three failure scenarios are implemented, each as a module with an `apply()` function:

- **`slow_database`** — calls `time.sleep(2)` to simulate a slow or overloaded database
- **`break_dns`** — simulates DNS resolution failure (currently a stub that logs the action)
- **`kill_services`** — simulates a service being terminated (currently a stub that logs the action)

A **runner** (`chaos/runner.py`) acts as a central dispatcher. It maps experiment names to their modules and exposes a single `run_experiment(name)` function. Calling it with an unknown name raises a `ValueError`, preventing silent failures.

### 3. Monitoring Layer (`monitor/`)

The monitor captures observability data during normal operation and chaos experiments:

- **`collector.py`** — stores request metrics (route, status code, response time) in memory, and provides `get_metrics()` and `get_error_count()` to query them
- **`dashboard.py`** — a thin wrapper that loads metrics from the collector, intended as the data source for a Streamlit dashboard

The app's `metrics.py` bridges the API layer to the monitor, so every HTTP request is automatically tracked via middleware.

### 4. Test Suites (`test/`)

27 automated tests across four files, all passing:

- **`test_orders.py`** (7 tests) — validates normal API behaviour: order creation, retrieval, listing, 404 handling, input validation, and DB failure handling
- **`test_chaos.py`** (7 tests) — validates that each chaos experiment can be triggered by name, that unknown experiments raise errors, and that each module's `apply()` function is callable
- **`test_monitor.py`** (6 tests) — validates that metrics are recorded correctly, response times are captured, error counts are tracked, and the dashboard can load metrics
- **`test_resilience.py`** (7 tests) — validates graceful degradation: DB timeouts return 503, the app recovers after a failure, concurrent requests are handled safely, slow DB responses complete within 10 seconds, and metrics are recorded on every order

### 5. Infrastructure

- **`Dockerfile`** — builds the app using `python:3.12-slim`, installs dependencies, and starts the server with `uvicorn`
- **`compose.yaml`** — defines two services: the FastAPI app on port 8000, and a PostgreSQL 16 database wired via `DATABASE_URL`

---

## Test Results

```
27 passed in 2.51s
```

All test suites pass. The one warning present (`httpx` vs `httpx2` deprecation) is a starlette internals notice and does not affect functionality.

---

## Known Limitations

- **In-memory storage** — orders and metrics are stored in Python dicts/lists. Data is lost on restart and is not connected to the PostgreSQL instance defined in `compose.yaml`.
- **Chaos stubs** — `break_dns` and `kill_services` currently print a message rather than performing real system-level actions.
- **No dashboard UI** — the Streamlit dashboard described in the README has not been built yet. The data pipeline is in place but there is no visual interface.
- **Shared state in tests** — `app/orders.py` uses module-level state that persists across tests. This works currently but could cause flaky tests if test order changes.

---

## How to Run

**Run the tests:**
```bash
python3 -m pytest test/ -v
```

**Start the server:**
```bash
python3 -m uvicorn app.main:app --reload
```

Then visit `http://localhost:8000/docs` for the interactive API explorer.

---

## Author

Lerato Tala
