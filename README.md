
# Real-Time IoT Anomaly Detection System

Real-time IoT monitoring platform built with **Python, FastAPI, MQTT, PostgreSQL, and React**, featuring asynchronous telemetry ingestion, statistical anomaly detection, and live WebSocket dashboards.

The project demonstrates an end-to-end, event-driven architecture capable of collecting telemetry from IoT devices, identifying anomalous readings, storing historical data, and visualizing events in real time.

## Dashboard

![Real-Time IoT Anomaly Detection Dashboard](assets/dashboard.png)

## API Documentation

![FastAPI Swagger Documentation](assets/swagger.png)

---

## Features

- **Real-time telemetry ingestion** through MQTT.
- **Asynchronous processing** using FastAPI and asyncio.
- **Statistical anomaly detection** using Z-score analysis.
- **Historical telemetry storage** with PostgreSQL.
- **Live dashboard updates** through WebSockets.
- **Interactive data visualization** with React and Recharts.
- **Device management** through REST API endpoints.
- **Automated database migrations** using Alembic.
- **MQTT telemetry simulator** for reproducible demonstrations.
- **Automated testing** with pytest and pytest-asyncio.
- **Code quality checks** using Ruff and mypy.
- **Containerized infrastructure** using Docker Compose or Podman.

---

## Architecture

The application follows a modular, event-driven architecture.

```text
                 IoT Devices / Simulator
                           |
                           | MQTT
                           v
                  +------------------+
                  | Mosquitto Broker |
                  +------------------+
                           |
                           v
                  +------------------+
                  |   MQTT Consumer  |
                  |  (Paho MQTT)     |
                  +------------------+
                           |
                           v
                  +------------------+
                  |   asyncio.Queue  |
                  +------------------+
                           |
                           v
                  +------------------+
                  | Ingestion Worker |
                  +------------------+
                           |
                           v
                  +------------------+
                  |  FastAPI Service |
                  +------------------+
                           |
                 +---------+---------+
                 |                   |
                 v                   v
        +----------------+  +------------------+
        |   PostgreSQL   |  | WebSocket Server |
        |   Persistence  |  |                  |
        +----------------+  +------------------+
                 ^                   |
                 |                   v
        +----------------+  +------------------+
        | Z-score        |  | React Dashboard  |
        | Detection      |  | Live Telemetry   |
        +----------------+  +------------------+
```

### Data Flow

1. An IoT device publishes telemetry to a predefined MQTT topic.
2. Mosquitto delivers the message to the MQTT consumer.
3. The consumer safely transfers the message from the MQTT callback thread to the application's asyncio queue.
4. An asynchronous worker processes the queued message.
5. The ingestion service validates the payload and resolves the device.
6. The anomaly detection service evaluates the reading against historical data.
7. PostgreSQL stores the telemetry event and its anomaly classification.
8. FastAPI broadcasts the event to connected WebSocket clients.
9. The React dashboard updates automatically without requiring a page refresh.

The REST API can also ingest telemetry directly, without passing through MQTT.

---

## Tech Stack

### Backend

| Technology | Purpose |
| --- | --- |
| Python 3.12 | Backend programming language |
| FastAPI | REST API and WebSocket server |
| SQLAlchemy Async | Asynchronous database operations |
| PostgreSQL 16 | Persistent telemetry storage |
| Alembic | Database schema migrations |
| Eclipse Mosquitto 2 | MQTT message broker |
| Paho MQTT | MQTT client and consumer |
| asyncio | Asynchronous queue and message processing |
| Pydantic | Data validation and configuration |
| Z-score | Statistical anomaly detection |

### Frontend

| Technology | Purpose |
| --- | --- |
| React | User interface |
| TypeScript | Type-safe frontend development |
| Vite | Frontend development and build tooling |
| Tailwind CSS | Styling |
| Recharts | Telemetry visualization |
| WebSockets | Live telemetry updates |

### Infrastructure and Development

| Technology | Purpose |
| --- | --- |
| Docker Compose / Podman | Local infrastructure |
| Redis 7 | Provisioned for future event-processing integrations |
| uv | Python dependency management |
| pytest | Automated testing |
| pytest-asyncio | Asynchronous testing |
| Ruff | Python linting and formatting |
| mypy | Static type checking |
| Git / GitHub | Version control |

> **Note:** The current anomaly detector uses statistical Z-score analysis, not a trained machine learning model. Redis is included in the development infrastructure but is not currently used as the telemetry event bus.

---

## Project Structure

```text
real-time-iot-anomaly-detection/
|
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   ├── core/
│   ├── db/
│   │   └── migrations/
│   ├── models/
│   ├── mqtt/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── websockets/
│   └── main.py
|
├── frontend/
│   └── src/
|
├── scripts/
│   └── publish_demo_sequence.py
|
├── tests/
│   └── api/
|
├── docker/
│   └── mosquitto/
|
├── assets/
│   ├── dashboard.png
│   └── swagger.png
|
├── .env.example
├── alembic.ini
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
└── README.md
```

### Main Components

- `app/main.py`: FastAPI application, middleware, and lifespan management.
- `app/mqtt/consumer.py`: MQTT connection, message queue, and asynchronous worker.
- `app/mqtt/ingestion.py`: MQTT payload processing and device resolution.
- `app/services/anomaly_detection.py`: Statistical anomaly detection.
- `app/services/telemetry_service.py`: Telemetry processing, persistence, and WebSocket broadcasting.
- `app/repositories/`: Database query and persistence operations.
- `app/websockets/`: WebSocket connections and broadcasting.
- `frontend/`: React monitoring dashboard.
- `scripts/`: Telemetry simulation utilities.
- `tests/`: Unit, integration, and regression tests.

---

## Getting Started

The following instructions describe how to run the application locally.

### 1. Prerequisites

Install the following tools:

- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- Node.js and npm
- Docker with Docker Compose, or Podman with a Compose provider
- Git

The application has been developed and tested locally on Fedora Linux using Podman.

### 2. Clone the Repository

```bash
git clone https://github.com/MarcMontolio/real-time-iot-anomaly-detection.git

cd real-time-iot-anomaly-detection
```

### 3. Configure Environment Variables

Create your local environment configuration.

Linux/macOS:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

For the default Docker Compose configuration, the relevant settings are:

```dotenv
APP_NAME=Real-Time IoT Anomaly Detection System
APP_ENV=development
DEBUG=true
API_V1_PREFIX=/api/v1

DATABASE_URL=postgresql+asyncpg://iot:iot@localhost:5433/iot_anomaly
DATABASE_SYNC_URL=postgresql+psycopg://iot:iot@localhost:5433/iot_anomaly

TEST_DATABASE_URL=postgresql+asyncpg://iot:iot@localhost:5433/iot_anomaly_test
TEST_DATABASE_SYNC_URL=postgresql+psycopg://iot:iot@localhost:5433/iot_anomaly_test

REDIS_URL=redis://localhost:6379/0

MQTT_HOST=localhost
MQTT_PORT=1883

LOG_LEVEL=INFO
```

These are local development settings and must match your infrastructure configuration.

> **Security:** The example credentials and anonymous MQTT access are intended only for local development. Do not expose these services directly to the internet or reuse the default credentials in production.

### 4. Install Backend Dependencies

Install the locked Python dependencies, including development tools:

```bash
uv sync --locked --extra dev --python 3.12
```

This creates a `.venv` virtual environment automatically.

Activate the environment on Linux/macOS:

```bash
source .venv/bin/activate
```

Or on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

All subsequent Python commands assume the virtual environment is activated and are executed from the repository root.

### 5. Start Infrastructure

The application requires PostgreSQL and Mosquitto. The Compose configuration also starts Redis.

Using Docker Compose:

```bash
docker compose up -d
```

Using Podman with a configured Compose provider:

```bash
podman compose up -d
```

### Infrastructure Ports

| Service | Host Port |
| --- | --- |
| PostgreSQL | 5433 |
| Redis | 6379 |
| Mosquitto MQTT | 1883 |

Verify the containers are running.

Docker:

```bash
docker compose ps
```

Podman:

```bash
podman compose ps
```

PostgreSQL data is stored in a persistent named volume.

### 6. Initialize the Databases

The PostgreSQL container creates the main database automatically when initialized with a fresh data volume:

```text
iot_anomaly
```

The automated tests use a separate database:

```text
iot_anomaly_test
```

Create the test database using Docker:

```bash
docker compose exec -T postgres \
  psql -U iot -d postgres \
  -c "CREATE DATABASE iot_anomaly_test;"
```

Or using Podman:

```bash
podman compose exec -T postgres \
  psql -U iot -d postgres \
  -c "CREATE DATABASE iot_anomaly_test;"
```

The test database only needs to be created once. Skip this command if it already exists.

### 7. Apply Database Migrations

Database schemas are managed through Alembic.

First, apply migrations to the main database:

```bash
python -m alembic upgrade head
```

Next, apply the same migrations to the test database.

Linux/macOS:

```bash
DATABASE_SYNC_URL="postgresql+psycopg://iot:iot@localhost:5433/iot_anomaly_test" \
  python -m alembic upgrade head
```

Windows PowerShell:

```powershell
$env:DATABASE_SYNC_URL = "postgresql+psycopg://iot:iot@localhost:5433/iot_anomaly_test"

python -m alembic upgrade head

Remove-Item Env:DATABASE_SYNC_URL
```

Both databases must have the latest migrations applied before running integration tests.

> **Important:** Integration tests delete existing telemetry and device records from the test database. Always keep testing and development data in separate databases.

### 8. Start the Backend

Run FastAPI:

```bash
uvicorn app.main:app --reload
```

The backend will be available at:

**http://127.0.0.1:8000**

Interactive API documentation:

**http://127.0.0.1:8000/docs**

Alternative API documentation:

**http://127.0.0.1:8000/redoc**

Health check:

```bash
curl http://127.0.0.1:8000/api/v1/health
```

Expected response:

```json
{
  "status": "ok"
}
```

The MQTT consumer starts automatically during the FastAPI application lifespan.

It subscribes to:

```text
iot/devices/+/telemetry
```

A separate MQTT consumer process is not required.

### 9. Start the Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The development dashboard will be available at:

**http://localhost:5173**

The dashboard connects to:

```text
ws://localhost:8000/ws/telemetry
```

It retrieves historical telemetry through the REST API and receives new events through WebSockets.

---

## Running the Demonstration

The repository includes a telemetry simulator for demonstrating MQTT ingestion and anomaly detection.

### 1. Register a Device

Before publishing MQTT telemetry, register a device through the REST API.

For example:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/devices \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "sensor-001",
    "name": "Demo Temperature Sensor",
    "device_type": "temperature",
    "location": "demo-lab"
  }'
```

The API returns the registered device and its internal database identifier.

Each external device ID must be unique. If the device already exists, skip registration.

### 2. Publish MQTT Telemetry

From the repository root, with the Python environment activated, execute:

```bash
python scripts/publish_demo_sequence.py
```

By default, the script publishes messages to:

```text
iot/devices/sensor-001/telemetry
```

To use another registered device:

```bash
python scripts/publish_demo_sequence.py --device-id sensor-004
```

The simulator publishes 15 temperature readings.

The sequence includes normal values around 40–43 °C and two intentionally anomalous readings:

```text
120.0 °C
130.0 °C
```

For a newly registered device with no existing telemetry, the expected demonstration result is:

| Metric | Expected Result |
| --- | --- |
| Published messages | 15 |
| Stored telemetry events | 15 |
| Normal readings | 13 |
| Anomalous readings | 2 |
| Detected anomalies | 120.0 °C and 130.0 °C |

Results may differ if the device already contains historical telemetry.

### 3. View the Dashboard

Open:

**http://localhost:5173**

The dashboard displays:

- WebSocket connection status.
- Total visible telemetry events.
- Normal event count.
- Anomalous event count.
- Percentage of anomalous visible events.
- Historical and live telemetry charts.
- A table of recent events.
- Anomaly scores and event classifications.

The dashboard currently displays a maximum of 50 recent events across devices.

New telemetry events should appear automatically without refreshing the browser.

### 4. Verify Stored Telemetry

Retrieve the latest events through the REST API:

```bash
curl "http://127.0.0.1:8000/api/v1/telemetry?limit=15"
```

The endpoint returns telemetry events ordered from newest to oldest.

---

## MQTT Message Format

Devices publish telemetry using the following topic structure:

```text
iot/devices/{device_id}/telemetry
```

Example:

```text
iot/devices/sensor-001/telemetry
```

### Example Payload

```json
{
  "metric_name": "temperature",
  "metric_value": 42.5,
  "timestamp": "2026-11-25T20:00:00Z"
}
```

### Fields

| Field | Type | Description |
| --- | --- | --- |
| `metric_name` | string | Name of the monitored metric |
| `metric_value` | number | Recorded metric value |
| `timestamp` | ISO 8601 string | UTC timestamp of the reading |

The device identifier is extracted from the MQTT topic.

The device must already be registered through the REST API.

---

## Anomaly Detection

The current anomaly detection mechanism uses statistical Z-score analysis.

For every incoming telemetry event, the service retrieves historical measurements associated with the same device and metric.

The Z-score is calculated using:

\[
z = \frac{x - \mu}{\sigma}
\]

Where:

- `x`: Current telemetry value.
- `μ`: Mean of historical values.
- `σ`: Standard deviation of historical values.

The default anomaly threshold is:

```text
abs(z_score) >= 3.0
```

Readings exceeding this threshold are classified as anomalies.

### Historical Data

The detector:

- Uses up to 50 previous measurements.
- Only compares readings from the same device and metric.
- Excludes previously classified anomalies from the historical baseline.
- Requires at least three historical measurements before evaluating anomalies.
- Stores the anomaly classification and calculated score with each event.

When there is insufficient valid history or the standard deviation cannot be used, the current implementation marks the event as non-anomalous with a score of `0.0`.

### Limitations

Z-score analysis provides a lightweight and interpretable statistical baseline, but it has limitations:

- It is sensitive to the distribution of historical measurements.
- It does not capture complex temporal patterns.
- It does not model seasonality or multivariate relationships.
- It requires sufficient historical data.
- It may not be suitable for all sensor types or operating conditions.

More advanced anomaly detection models are potential future improvements.

---

## REST API

FastAPI provides interactive OpenAPI documentation at:

```text
http://127.0.0.1:8000/docs
```

### Available Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/devices` | Register a device |
| GET | `/api/v1/devices` | List registered devices |
| GET | `/api/v1/devices/{device_id}` | Retrieve a device by external ID |
| GET | `/api/v1/devices/{device_id}/telemetry` | Retrieve telemetry using the internal numeric device ID |
| POST | `/api/v1/telemetry` | Create a telemetry event |
| GET | `/api/v1/telemetry` | Retrieve historical telemetry events |

### Example: Create Telemetry Through REST

The REST API uses the internal numeric device identifier.

For example:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/telemetry \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": 1,
    "metric_name": "temperature",
    "metric_value": 42.5,
    "timestamp": "2026-11-25T20:00:00Z"
  }'
```

Replace `1` with the internal ID returned when registering your device.

Telemetry created through the REST API also passes through the anomaly detection service and is broadcast to connected WebSocket clients.

### Pagination

The telemetry listing endpoint supports:

```text
GET /api/v1/telemetry?limit=50&offset=0
```

Events are returned from newest to oldest.

---

## WebSocket API

The application provides a WebSocket endpoint:

```text
ws://localhost:8000/ws/telemetry
```

Connected clients receive telemetry events after they have been successfully stored.

### Example Event

```json
{
  "id": 78,
  "device_id": 4,
  "metric_name": "temperature",
  "metric_value": 42.7,
  "timestamp": "2026-11-25T20:22:48+00:00",
  "is_anomaly": false,
  "anomaly_score": 1.3798879149488883
}
```

WebSockets are used to update the React interface without repeatedly polling the REST API.

The REST API remains available for retrieving historical data.

---

## Testing

The project includes automated unit, integration, and regression tests.

### Run All Tests

Ensure PostgreSQL, Mosquitto, and the dedicated test database are available.

Execute:

```bash
python -m pytest -v
```

For a more compact output:

```bash
python -m pytest -q --disable-warnings
```

### Test Coverage Areas

The current test suite covers:

- REST API health checks.
- Device registration and validation.
- Telemetry creation and retrieval.
- API parameter validation.
- Statistical calculations.
- Anomaly detection.
- MQTT topic and payload parsing.
- MQTT telemetry ingestion.
- Asynchronous MQTT message processing.
- Consecutive message handling across threads.
- Historical telemetry ordering.
- Database integration.

### Regression Tests

Two important regression scenarios are included.

**MQTT message processing**

Verifies that 15 consecutive MQTT messages can be transferred from an MQTT callback thread to the application's asyncio queue without losing or duplicating messages.

**Historical telemetry ordering**

Verifies that the telemetry API returns the most recent events first, even when records are inserted in a different chronological order.

### Last Verified Local Results

```text
37 passed
```

Some dependency-related deprecation warnings may still appear during testing.

---

## Code Quality

### Ruff Linting

```bash
ruff check .
```

### Ruff Formatting

Check formatting without modifying files:

```bash
ruff format --check .
```

Format an individual file:

```bash
ruff format path/to/file.py
```

### Static Type Checking

```bash
mypy app
```

Static type checking is available as a development tool; passing results are not claimed here.

### Git Whitespace Checks

```bash
git diff --check
```

---

## Infrastructure Notes

### PostgreSQL

PostgreSQL stores:

- Registered devices.
- Telemetry measurements.
- Event timestamps.
- Anomaly classifications.
- Anomaly scores.

The database schema is managed by Alembic.

The main and test databases must remain separate.

### MQTT

Mosquitto acts as the MQTT broker.

The backend subscribes to telemetry topics and processes messages through an asynchronous queue.

This design avoids executing asynchronous database operations directly inside the Paho MQTT callback thread.

### Redis

Redis is provisioned in Docker Compose for potential future extensions.

It is not currently part of the active telemetry ingestion pipeline.

### Docker and Podman

Docker Compose or Podman can be used to start the supporting infrastructure.

The FastAPI backend and React frontend currently run locally outside the infrastructure containers.

The Compose configuration is intended for development, not production deployment.

---

## Example Use Cases

The architecture can be adapted for several monitoring scenarios:

- Industrial IoT sensor monitoring.
- Smart building telemetry.
- Environmental measurements.
- Equipment condition monitoring.
- Temperature and humidity monitoring.
- Real-time operational dashboards.
- Statistical anomaly detection in sensor networks.

---

## Future Improvements

Potential extensions include:

- Redis Streams or another event bus for distributed processing.
- Kafka integration for higher-throughput telemetry.
- Advanced machine learning anomaly detection.
- Multivariate and time-series analysis.
- Authentication and role-based access control.
- Device-specific dashboard filters.
- Historical analytics and configurable time ranges.
- Improved WebSocket connection management and reconnection handling.
- Structured application logging and observability.
- Prometheus and Grafana monitoring.
- Containerization of the backend and frontend.
- Continuous integration and deployment pipelines.
- Production-ready MQTT authentication and TLS.
- Kubernetes deployment.

These are potential improvements rather than features currently implemented.

---

## License

This project is released under the MIT License.
