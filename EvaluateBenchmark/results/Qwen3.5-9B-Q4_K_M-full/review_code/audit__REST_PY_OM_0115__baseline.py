import requests

def solve(inputs):
    """
    Retrieves hourly relative humidity at two metres and precipitation from the Open-Meteo public API
    for a given location, covering three forecast days.

    Args:
        inputs (dict): A dictionary containing 'latitude' and 'longitude'.

    Returns:
        dict or None: The decoded JSON response if successful. Returns None for an empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    # Open-Meteo API endpoint for hourly weather forecast
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
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for an empty response (e.g., no data available)
    if not data.get('hourly'):
        return None
    
    return data