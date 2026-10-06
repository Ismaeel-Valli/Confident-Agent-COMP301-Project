import requests

def solve(inputs):
    """
    Retrieve hourly relative humidity at two metres and precipitation from Open-Meteo public API.
    
    Args:
        inputs (dict): A dictionary containing 'latitude' and 'longitude'.
        
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'relative_humidity_2m,precipitation',
        'forecast_days': 3,
        'timezone': 'auto'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP request failed with status code {response.status_code}")
    
    data = response.json()
    
    # Return None for a successful empty response
    if not data or (isinstance(data, dict) and not any(data.values())):
        return None
        
    return data