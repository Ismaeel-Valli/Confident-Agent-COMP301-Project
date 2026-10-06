import requests

def solve(inputs):
    """
    Retrieve hourly temperature at 2m and precipitation from Open-Meteo API for three forecast days.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    latitude = inputs["latitude"]
    longitude = inputs["longitude"]
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation",
        "forecast_days": 3
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    if not data:
        return None
    
    return data