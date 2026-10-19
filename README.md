WTC-WA8RS3TA

# chaos-kitchen

## Overview

Chaos Kitchen is a beginner-friendly chaos engineering project that tests how an application behaves when failures occur. It uses a simple food-ordering application to simulate problems and observe how the system responds and recovers.

## Objectives

- Build a simple food-ordering API.
- Simulate application and database failures.
- Monitor application health and performance.
- Measure errors, response times, and recovery time.
- Test ways to improve application reliability.

## Technologies

- Python
- FastAPI
- PostgreSQL
- Docker and Docker Compose
- pytest
- pandas
- Streamlit

## Planned Features

- Food-ordering API
- Health monitoring
- Controlled failure simulations
- Metrics collection
- Monitoring dashboard
- Automated tests
- Recovery and resilience testing

## Getting Started

### Prerequisites

Install Python, Git, and Docker.

### Setup

Clone the repository:

```bash
git clone https://github.com/LeratoTala/chaos-kitchen
cd chaos-kitchen
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies once `requirements.txt` is available:

```bash
pip install -r requirements.txt
```

## Running the Project

The easiest way to run the project is with Docker Compose. Make sure Docker is installed and running, then from the project root:

```bash
docker compose up --build
```

This starts the app and a PostgreSQL database together. Once running:

- API: http://localhost:8000
- Interactive API docs: http://localhost:8000/docs

To stop the project:

```bash
docker compose down
```

## Chaos Experiments

The project will explore:

- Application service failures
- Database unavailability
- Increased database latency
- Recovery after failures

All experiments will run in a controlled local environment.


## Safety

Chaos experiments must only run against dedicated local test services, never production systems.

## Author

Lerato Tala
