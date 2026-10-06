import requests

def solve(inputs):
    """
    Retrieve hourly relative humidity at 2m and wind speed at 10m from Open-Meteo,
    using the automatically determined time zone, for a forecast covering three days.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response. Returns None if successful but empty.
                      Raises an exception on unsuccessful HTTP response.
    """
    latitude = inputs["latitude"]
    longitude = inputs["longitude"]
    
    base_url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "relative_humidity_2m,wind_speed_10m",
        "timezone": "auto",
        "forecast_days": 3
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data