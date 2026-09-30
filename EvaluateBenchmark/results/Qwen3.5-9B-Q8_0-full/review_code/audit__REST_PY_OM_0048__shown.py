import requests

def solve(inputs):
    """
    Retrieve hourly wind wave height from Open-Meteo marine forecast service.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    lat = inputs['latitude']
    lon = inputs['longitude']
    
    url = "https://marine-api.open-meteo.com/v1/marine"
    params = {
        'latitude': lat,
        'longitude': lon,
        'hourly': 'wind_wave_height',
        'timezone': 'auto',
        'forecast_days': 3
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    if not data:
        return None
    
    return data