import requests

def solve(inputs):
    """
    Retrieve hourly temperature at two metres and wind speed at ten metres
    from Open-Meteo public API using the weather forecast service.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.open-meteo.com"
    endpoint = "/v1/forecast"
    
    lat = inputs["latitude"]
    lon = inputs["longitude"]
    
    url = f"{base_url}{endpoint}?latitude={lat}&longitude={lon}&hourly=temperature_2m,wind_speed_10m"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data