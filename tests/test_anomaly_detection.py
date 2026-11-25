import pytest

from app.services.anomaly_detection import (
    calculate_mean,
    calculate_standard_deviation,
    calculate_z_score,
    detect_anomaly,
)


def test_calculate_mean_returns_correct_average() -> None:
    values = [10.0, 20.0, 30.0]
    
    result = calculate_mean(values)
    
    assert result == 20.0
    

def test_calculate_mean_empty_list_returns_error() -> None:
    values = []
    
    with pytest.raises(ValueError):
        calculate_mean(values)
        

def test_calculate_standard_deviation_returns_correct_value() -> None:
    values = [10.0, 20.0, 30.0]
    result = calculate_standard_deviation(values)
    rounded_result = round(result, 2)
    assert rounded_result == 8.16
    

def test_calculate_standard_deviation_empty_list_returns_error() -> None:
    values = []
    
    with pytest.raises(ValueError):
        calculate_standard_deviation(values)


def test_calculate_z_score_returns_correct_value() -> None:
    value = 30
    mean = 20
    standard_deviation = 5
    
    result = calculate_z_score(value, mean, standard_deviation)
    
    assert result == 2.0
    

def test_calculate_z_score_standard_deviation_is_zero_returns_error() -> None:
    value = 30
    mean = 20
    standard_deviation = 0
    
    with pytest.raises(ValueError):
        calculate_z_score(value, mean, standard_deviation)
        
        
def test_detect_anomaly_returns_false_for_normal_value() -> None:
    historical_values = [10, 11, 12, 13, 14]
    value = 12
    threshold = 3.0
    
    is_anomaly, z_score = detect_anomaly(value, historical_values, threshold)
    
    assert is_anomaly is False
    assert isinstance(z_score, float)


def test_detect_anomaly_returns_true_for_abnormal_value() -> None:
    historical_values = [10, 11, 12, 13, 14]
    value = 100
    threshold = 3.0
    
    is_anomaly, z_score = detect_anomaly(value, historical_values, threshold)
    
    assert is_anomaly is True
    assert abs(z_score) >= threshold
    

def test_detect_anomaly_empty_list_returns_error() -> None:
    historical_values = []
    value = 100
    threshold = 3.0
    
    with pytest.raises(ValueError):
        detect_anomaly(value, historical_values, threshold)