import requests

def solve(inputs):
    """
    Retrieve hourly PM10 forecast from Open-Meteo air quality API.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response. None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    lat = inputs['latitude']
    lon = inputs['longitude']
    
    url = "https://api.open-meteo.com/v1/air-quality"
    params = {
        'latitude': lat,
        'longitude': lon,
        'hourly': 'pm10'
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    # Return None if the hourly data is empty (e.g., no forecast available)
    if not data.get('hourly', {}).get('pm10'):
        return None
    
    return data