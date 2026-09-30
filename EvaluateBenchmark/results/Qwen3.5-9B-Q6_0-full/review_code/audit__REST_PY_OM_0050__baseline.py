import requests

def solve(inputs):
    """
    Retrieves hourly ozone data from Open-Meteo public API based on provided coordinates.
    
    Args:
        inputs (dict): A dictionary containing 'latitude' and 'longitude'.
        
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
        
    Raises:
        requests.RequestException: If the HTTP request is unsuccessful.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "o3",  # Ozone concentration
        "timezone": "auto"
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise requests.RequestException(f"API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Check if the hourly data for ozone is empty or missing
    if 'hourly' not in data or len(data['hourly']) == 0:
        return None
        
    return data