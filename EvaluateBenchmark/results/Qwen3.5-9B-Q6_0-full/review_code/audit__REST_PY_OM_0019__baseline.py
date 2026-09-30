import requests

def solve(inputs):
    """
    Retrieves hourly relative humidity at two metres from Open-Meteo public API.
    
    Args:
        inputs (dict): Dictionary containing 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response, or None if the response is successfully empty.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "relative_humidity_2m",
        "forecast_days": 3
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Check if the hourly data is empty (e.g., no valid forecast points returned)
    if 'hourly' not in data or len(data['hourly'].get('relative_humidity_2m', [])) == 0:
        return None
        
    return data