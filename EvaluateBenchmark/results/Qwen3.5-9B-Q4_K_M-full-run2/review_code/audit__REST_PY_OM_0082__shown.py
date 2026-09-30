import requests

def solve(inputs):
    """
    Retrieve hourly temperature at two metres and precipitation from Open-Meteo,
    using the location's automatically determined time zone, covering three forecast days.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response. Returns None for a successful empty response.
        
    Raises:
        Exception: For an unsuccessful HTTP response.
    """
    lat = inputs['latitude']
    lon = inputs['longitude']
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,precipitation",
        "timezone": "auto",
        "forecast_days": 3
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    if not response.text.strip():
        return None
    
    return response.json()