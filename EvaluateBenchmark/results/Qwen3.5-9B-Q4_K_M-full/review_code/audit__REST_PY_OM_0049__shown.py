def solve(inputs):
    """
    Retrieve hourly cloud cover from Open-Meteo weather forecast service.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response, or None if the response is empty.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    import requests
    
    base_url = "https://api.open-meteo.com"
    endpoint = "/v1/forecast"
    
    params = {
        "latitude": inputs["latitude"],
        "longitude": inputs["longitude"],
        "hourly": "cloud_cover"
    }
    
    url = f"{base_url}{endpoint}"
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    return data if not data else None