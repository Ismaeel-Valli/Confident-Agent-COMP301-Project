import requests

def solve(inputs):
    """
    Retrieves hourly wind wave height from Open-Meteo marine forecast service.
    
    Args:
        inputs (dict): Dictionary containing 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response, or None if the response is successful but empty.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'wind_speed_10m',
        'marine': 'wave_height',
        'timezone': 'auto'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP request failed with status code: {response.status_code}")
    
    data = response.json()
    
    # Return None for a successful empty response (e.g., no hourly data available)
    if not data or 'hourly' not in data:
        return None
        
    return data