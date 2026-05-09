import json
from typing import cast


def extract_device_id_from_topic(topic: str) -> str:
    parts = topic.split("/")

    if len(parts) != 4:
        raise ValueError("Invalid MQTT topic format")

    if parts[0] != "iot" or parts[1] != "devices" or parts[3] != "telemetry":
        raise ValueError("Invalid MQTT topic format")

    return parts[2]


def parse_telemetry_payload(payload: str) -> dict[str, object]:
    try:
        parsed_payload = json.loads(payload)
    except json.JSONDecodeError:
        raise ValueError("An error occurred during parsing to JSON")

    if not isinstance(parsed_payload, dict):
        raise ValueError("The parsed JSON is not an object")

    json_payload = cast(dict[str, object], parsed_payload)

    required_fields = {
        "metric_name",
        "metric_value",
        "timestamp",
    }

    if not required_fields.issubset(json_payload):
        raise ValueError("Some mandatory fields are missing")

    return json_payload