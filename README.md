# Real-Time IoT Anomaly Detection System

Event-driven backend platform for real-time IoT telemetry ingestion, anomaly detection and live alerting using FastAPI, MQTT, Redis, PostgreSQL and machine learning.

## Overview

The goal of this project is to demonstrate production-oriented backend engineering practices applied to real-time IoT monitoring and anomaly detection systems.

This project aims to simulate and monitor IoT devices in real time, process telemetry streams and detect anomalous behaviour using machine learning models.

The platform is being designed with a production-oriented architecture focused on backend engineering, event-driven systems and observability.

Current features include:

- FastAPI backend
- Modular API architecture
- Health check endpoint
- Automated testing with pytest
- Static analysis with Ruff and mypy
- Typed Python codebase
- Environment-based configuration with pydantic-settings

## Planned Architecture

```text
IoT Devices / Simulator
        |
        v
     MQTT Broker
        |
        v
 Ingestion Worker
        |
        +--> PostgreSQL
        |
        +--> Redis Pub/Sub
                    |
                    v
       Anomaly Detection Worker
                    |
                    v
              WebSocket API
                    |
                    v
           Real-time Dashboard
```

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- Redis
- MQTT
- Docker
- WebSockets
- scikit-learn
- pytest
- Ruff
- mypy

## Project Structure

```text
app/
├── api/
├── core/
└── main.py

tests/
```

## Getting Started

### Create virtual environment

```bash
python -m venv .venv
```

### Activate virtual environment

Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

Linux/macOS

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -e ".[dev]"
```

### Run the API

```bash
uvicorn app.main:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## Running Tests

```bash
pytest -v
```

## Current API Endpoints

| Method | Endpoint       | Description  |
|--------|----------------|--------------|
| GET    | /api/v1/health | Health check |

## Roadmap

- MQTT ingestion worker
- PostgreSQL integration
- Redis event bus
- IoT simulator
- Streaming anomaly detection
- Real-time WebSocket dashboard
- Docker Compose deployment
- Metrics and observability
- Kafka integration
- Advanced ML models

## Development Philosophy

This project is intentionally being built using production-oriented engineering practices:

- Modular architecture
- Typed Python
- Separation of concerns
- Test-first mindset
- Event-driven design
- Scalable backend patterns
- Infrastructure reproducibility

## License

MIT
