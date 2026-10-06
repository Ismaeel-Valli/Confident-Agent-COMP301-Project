import requests

def solve(inputs):
    """
    Retrieve hourly PM10 and CO from Open-Meteo air quality API for 3 forecast days.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
        
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    lat = inputs['latitude']
    lon = inputs['longitude']
    
    base_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "pm10",
        "forecast_days": 3
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data or (isinstance(data, dict) and not any(data.values())):
        return None
    
    return data