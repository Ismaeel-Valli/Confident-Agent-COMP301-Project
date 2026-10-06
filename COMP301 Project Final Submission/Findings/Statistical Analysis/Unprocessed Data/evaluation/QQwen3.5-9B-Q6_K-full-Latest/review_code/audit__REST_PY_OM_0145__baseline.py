import requests

def solve(inputs):
    """
    Retrieves hourly precipitation and wind speed at 10m from Open-Meteo API.
    
    Args:
        inputs (dict): Dictionary containing 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
        
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'precipitation,windspeed_10m',
        'timezone': 'auto'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Check if the hourly data is empty (e.g., no valid forecast points)
    if 'hourly' not in data or len(data['hourly'].keys()) == 0:
        return None
        
    return data