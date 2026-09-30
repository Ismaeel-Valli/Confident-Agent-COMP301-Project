import requests

def solve(inputs):
    """
    Retrieve hourly PM10 forecast from Open-Meteo air quality API.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    lat = inputs['latitude']
    lon = inputs['longitude']
    
    url = "https://api.open-meteo.com/v1/air-quality"
    params = {
        'latitude': lat,
        'longitude': lon,
        'hourly': 'pm10',
        'forecast_days': 1
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    data = response.json()
    return data