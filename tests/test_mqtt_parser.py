import pytest

from app.mqtt.parser import extract_device_id_from_topic, parse_telemetry_payload


def test_extract_device_id_from_valid_topic() -> None:
    topic = "iot/devices/sensor-001/telemetry"
    
    result = extract_device_id_from_topic(topic)
    
    assert result == "sensor-001"
    
    

def test_extract_device_id_from_invalid_topic_raises_value_error() -> None:
    topic = "..."

    with pytest.raises(ValueError):
        extract_device_id_from_topic(topic)
        

def test_parse_telemetry_payload_returns_dict() -> None:
    payload = """
    {
        "metric_name": "temperature",
        "metric_value": 42.5,
        "timestamp": "2026-05-09T12:00:00Z"
    }
    """
    
    result = parse_telemetry_payload(payload)
    
    assert isinstance(result, dict)
    
def test_parse_telemetry_wrong_payload_returns_error() -> None:
    payload = """
    No JSON here
    """
    
    with pytest.raises(ValueError):
        parse_telemetry_payload(payload)
        
        
def test_parse_telemetry_incomplete_payload_returns_error() -> None:
    payload = """
    {
        "metric_name": "temperature",
        "metric_value": 42.5
    }
    """
    
    with pytest.raises(ValueError):
        parse_telemetry_payload(payload)
    
    
def test_parse_telemetry_payload_not_a_dict_error() -> None:
    payload = """[1, 2, 3]"""
    
    with pytest.raises(ValueError):
        parse_telemetry_payload(payload)
    