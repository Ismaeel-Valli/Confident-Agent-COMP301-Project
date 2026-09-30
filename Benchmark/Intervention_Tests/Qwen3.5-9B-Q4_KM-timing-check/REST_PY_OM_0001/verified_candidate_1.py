import requests

def solve(inputs):
    """
    Retrieve hourly temperature at two metres from Open-Meteo public API.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.open-meteo.com"
    endpoint = "/v1/forecast"
    
    params = {
        "latitude": inputs["latitude"],
        "longitude": inputs["longitude"],
        "hourly": "temperature_2m",
        "format": "json"
    }
    
    url = f"{base_url}{endpoint}"
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data