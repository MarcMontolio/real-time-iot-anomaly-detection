# Details

Date : 2026-05-10 17:37:40

Directory c:\\Users\\mmc14\\Documents\\GitHub\\real-time-iot-anomaly-detection

Total : 54 files,  1455 codes, 66 comments, 558 blanks, all 2079 lines

[Summary](results.md) / Details / [Diff Summary](diff.md) / [Diff Details](diff-details.md)

## Files
| filename | language | code | comment | blank | total |
| :--- | :--- | ---: | ---: | ---: | ---: |
| [README.md](/README.md) | Markdown | 113 | 0 | 40 | 153 |
| [alembic.ini](/alembic.ini) | Ini | 123 | 0 | 27 | 150 |
| [app/\_\_init\_\_.py](/app/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [app/api/\_\_init\_\_.py](/app/api/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [app/api/deps.py](/app/api/deps.py) | Python | 6 | 0 | 4 | 10 |
| [app/api/v1/\_\_init\_\_.py](/app/api/v1/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [app/api/v1/endpoints/\_\_init\_\_.py](/app/api/v1/endpoints/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [app/api/v1/endpoints/devices.py](/app/api/v1/endpoints/devices.py) | Python | 55 | 0 | 12 | 67 |
| [app/api/v1/endpoints/health.py](/app/api/v1/endpoints/health.py) | Python | 5 | 8 | 6 | 19 |
| [app/api/v1/endpoints/telemetry.py](/app/api/v1/endpoints/telemetry.py) | Python | 27 | 0 | 5 | 32 |
| [app/api/v1/router.py](/app/api/v1/router.py) | Python | 11 | 0 | 4 | 15 |
| [app/core/\_\_init\_\_.py](/app/core/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [app/core/config.py](/app/core/config.py) | Python | 19 | 0 | 3 | 22 |
| [app/db/\_\_init\_\_.py](/app/db/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [app/db/base.py](/app/db/base.py) | Python | 3 | 0 | 3 | 6 |
| [app/db/migrations/env.py](/app/db/migrations/env.py) | Python | 37 | 29 | 17 | 83 |
| [app/db/migrations/versions/22cd412f5a6a\_create\_telemetry\_events\_table.py](/app/db/migrations/versions/22cd412f5a6a_create_telemetry_events_table.py) | Python | 24 | 14 | 8 | 46 |
| [app/db/migrations/versions/eaba4cf93ef5\_create\_devices\_table.py](/app/db/migrations/versions/eaba4cf93ef5_create_devices_table.py) | Python | 25 | 14 | 8 | 47 |
| [app/db/models.py](/app/db/models.py) | Python | 4 | 0 | 2 | 6 |
| [app/db/session.py](/app/db/session.py) | Python | 12 | 0 | 4 | 16 |
| [app/main.py](/app/main.py) | Python | 9 | 0 | 4 | 13 |
| [app/models/\_\_init\_\_.py](/app/models/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [app/models/device.py](/app/models/device.py) | Python | 29 | 0 | 6 | 35 |
| [app/models/telemetry\_event.py](/app/models/telemetry_event.py) | Python | 25 | 0 | 9 | 34 |
| [app/mqtt/\_\_init\_\_.py](/app/mqtt/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [app/mqtt/consumer.py](/app/mqtt/consumer.py) | Python | 41 | 0 | 21 | 62 |
| [app/mqtt/ingestion.py](/app/mqtt/ingestion.py) | Python | 30 | 1 | 14 | 45 |
| [app/mqtt/parser.py](/app/mqtt/parser.py) | Python | 25 | 0 | 12 | 37 |
| [app/repositories/\_\_init\_\_.py](/app/repositories/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [app/repositories/device\_repository.py](/app/repositories/device_repository.py) | Python | 39 | 0 | 12 | 51 |
| [app/repositories/telemetry\_repository.py](/app/repositories/telemetry_repository.py) | Python | 59 | 0 | 11 | 70 |
| [app/schemas/\_\_init\_\_.py](/app/schemas/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [app/schemas/device.py](/app/schemas/device.py) | Python | 17 | 0 | 6 | 23 |
| [app/schemas/telemetry\_event.py](/app/schemas/telemetry_event.py) | Python | 17 | 0 | 7 | 24 |
| [app/services/\_\_init\_\_.py](/app/services/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [app/services/anomaly\_detection.py](/app/services/anomaly_detection.py) | Python | 37 | 0 | 19 | 56 |
| [app/services/device\_service.py](/app/services/device_service.py) | Python | 40 | 0 | 11 | 51 |
| [app/services/telemetry\_service.py](/app/services/telemetry_service.py) | Python | 61 | 0 | 18 | 79 |
| [docker-compose.yml](/docker-compose.yml) | YAML | 27 | 0 | 4 | 31 |
| [docker/mosquitto/mosquitto.conf](/docker/mosquitto/mosquitto.conf) | Properties | 2 | 0 | 0 | 2 |
| [scripts/mqtt\_publisher.py](/scripts/mqtt_publisher.py) | Python | 20 | 0 | 10 | 30 |
| [scripts/mqtt\_subscriber.py](/scripts/mqtt_subscriber.py) | Python | 29 | 0 | 14 | 43 |
| [scripts/publish\_test\_message.py](/scripts/publish_test_message.py) | Python | 14 | 0 | 2 | 16 |
| [scripts/run\_consumer.py](/scripts/run_consumer.py) | Python | 2 | 0 | 1 | 3 |
| [tests/\_\_init\_\_.py](/tests/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [tests/api/\_\_init\_\_.py](/tests/api/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [tests/api/v1/\_\_init\_\_.py](/tests/api/v1/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [tests/api/v1/test\_devices.py](/tests/api/v1/test_devices.py) | Python | 116 | 0 | 52 | 168 |
| [tests/api/v1/test\_health.py](/tests/api/v1/test_health.py) | Python | 8 | 0 | 5 | 13 |
| [tests/api/v1/test\_telemetry\_events.py](/tests/api/v1/test_telemetry_events.py) | Python | 149 | 0 | 66 | 215 |
| [tests/conftest.py](/tests/conftest.py) | Python | 44 | 0 | 19 | 63 |
| [tests/test\_anomaly\_detection.py](/tests/test_anomaly_detection.py) | Python | 51 | 0 | 31 | 82 |
| [tests/test\_mqtt\_ingestion.py](/tests/test_mqtt_ingestion.py) | Python | 61 | 0 | 25 | 86 |
| [tests/test\_mqtt\_parser.py](/tests/test_mqtt_parser.py) | Python | 39 | 0 | 22 | 61 |

[Summary](results.md) / Details / [Diff Summary](diff.md) / [Diff Details](diff-details.md)