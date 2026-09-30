import requests

def solve(inputs):
    """
    Retrieve hourly wave height from Open-Meteo marine forecast service.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    url = "https://marine-api.open-meteo.com/v1/marine"
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'wave_height',
        'timezone': 'auto',
        'forecast_days': 3
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    data = response.json()
    return data