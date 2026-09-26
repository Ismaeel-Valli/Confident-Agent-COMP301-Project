import requests

def solve(inputs):
    """
    Retrieves hourly PM10 forecast data from Open-Meteo public API.
    
    Args:
        inputs (dict): Dictionary containing 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response.
        
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'pm10',
        'timezone': 'auto'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (e.g., no hourly PM10 data available)
    if not data.get('hourly'):
        return None
        
    return data