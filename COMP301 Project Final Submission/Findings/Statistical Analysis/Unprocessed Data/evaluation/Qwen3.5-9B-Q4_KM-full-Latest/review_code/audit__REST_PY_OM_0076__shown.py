def solve(inputs):
    """
    Retrieve hourly temperature at two metres and precipitation from Open-Meteo public API.
    
    Args:
        inputs (dict): Dictionary containing:
            - latitude (float): Geographical WGS84 coordinates (latitude)
            - longitude (float): Longitude
    
    Returns:
        dict or None: Decoded JSON response, or None for a successful empty response
    
    Raises:
        Exception: For an unsuccessful HTTP response
    """
    import requests
    
    lat = inputs["latitude"]
    lon = inputs["longitude"]
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,precipitation",
        "timezone": "auto"
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    # Return None for a successful empty response (no hourly data)
    if not data.get("hourly"):
        return None
    
    return data