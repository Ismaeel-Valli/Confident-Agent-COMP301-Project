import requests

def solve(inputs):
    """
    Retrieve hourly cloud cover from Open-Meteo weather forecast service.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'cloud_cover',
        'forecast_days': 3
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    if not data:
        return None
    
    return data