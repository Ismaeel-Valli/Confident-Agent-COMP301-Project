import requests

def solve(inputs):
    """
    Retrieve hourly temperature at two metres from Open-Meteo weather forecast service.
    
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
        'hourly': 'temperature_2m',
        'format': 'json'
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    return response.json()