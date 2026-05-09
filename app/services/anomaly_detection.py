import math


def calculate_mean(values: list[float]) -> float:
    if not values:
        raise ValueError("List of values is empty")
    
    values_sum = sum(values)
    values_length = len(values)
    
    mean = values_sum / values_length
    return mean


def calculate_standard_deviation(values: list[float]) -> float:
    if not values:
        raise ValueError("List of values is empty")
    
    mean = calculate_mean(values)
    
    squared_differences = []
    
    for value in values:
        squared_difference = (value - mean) ** 2
        squared_differences.append(squared_difference)
        
    variance = sum(squared_differences) / len(squared_differences)
    
    standard_deviation = math.sqrt(variance)
    return standard_deviation


def calculate_z_score(
    value: float,
    mean: float,
    standard_deviation: float
) -> float:
    
    if standard_deviation == 0:
        raise ValueError("Standard deviation cannot be 0")
    
    z_score = (value - mean) / standard_deviation
    return z_score


def detect_anomaly(
    value: float,
    historical_values: list[float],
    threshold: float = 3.0,
) -> tuple[bool, float]:
    
    mean = calculate_mean(historical_values)
    standard_deviation = calculate_standard_deviation(historical_values)
    z_score = calculate_z_score(value, mean, standard_deviation)
    
    return abs(z_score) >= threshold, z_score