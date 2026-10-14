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
git clone <YOUR-GITHUB-REPOSITORY-URL>
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

## Chaos Experiments

The project will explore:

- Application service failures
- Database unavailability
- Increased database latency
- Recovery after failures

All experiments will run in a controlled local environment.

## Project Status

The project is currently in development. Features will be added and tested step by step.

## Safety

Chaos experiments must only run against dedicated local test services, never production systems.

## Author

Lerato Tala
