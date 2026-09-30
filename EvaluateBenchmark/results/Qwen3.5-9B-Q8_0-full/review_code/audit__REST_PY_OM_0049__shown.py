import requests

def solve(inputs):
    """
    Retrieve hourly cloud cover from Open-Meteo weather forecast service.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
        
    Raises:
        requests.RequestException: For unsuccessful HTTP responses.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'cloud_cover'
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    data = response.json()
    return data