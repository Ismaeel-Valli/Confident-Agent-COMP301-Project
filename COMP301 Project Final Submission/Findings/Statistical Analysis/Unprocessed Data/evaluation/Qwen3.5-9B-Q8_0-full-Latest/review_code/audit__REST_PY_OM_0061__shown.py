import requests

def solve(inputs):
    """
    Retrieve hourly temperature at 2m and relative humidity at 2m from Open-Meteo.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response, or None if response is empty but successful.
        
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    lat = inputs["latitude"]
    lon = inputs["longitude"]
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m",
        "timezone": "auto"
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    try:
        data = response.json()
        return data
    except ValueError:
        raise Exception(f"Failed to decode JSON response from Open-Meteo API")