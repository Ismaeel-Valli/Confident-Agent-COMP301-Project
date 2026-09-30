import requests

def solve(inputs):
    """
    Retrieve hourly relative humidity at two metres from Open-Meteo weather forecast service.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'relative_humidity_2m',
        'timezone': 'auto',
        'forecast_days': 3
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    return response.json()