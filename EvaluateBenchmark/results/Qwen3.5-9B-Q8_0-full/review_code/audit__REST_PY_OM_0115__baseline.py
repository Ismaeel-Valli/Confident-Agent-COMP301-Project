import requests

def solve(inputs):
    """
    Retrieves hourly relative humidity at two metres and precipitation 
    from the Open-Meteo public API for three forecast days.
    
    Args:
        inputs (dict): A dictionary containing 'latitude' and 'longitude'.
        
    Returns:
        dict or None: The decoded JSON response, or None if the response is empty.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "relative_humidity_2m,precipitation",
        "forecast_days": 3,
        "timezone": "auto"
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Check if the response is empty (e.g., no hourly data available)
    if not data.get("hourly"):
        return None
        
    return data