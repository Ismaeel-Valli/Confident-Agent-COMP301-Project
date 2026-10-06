import requests

def solve(inputs):
    """
    Retrieves hourly relative humidity at two metres from Open-Meteo API.
    
    Args:
        inputs (dict): Dictionary containing 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response, or None if the response is empty but successful.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    # Construct the URL with parameters for 3 days of hourly relative humidity at 2m
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'relative_humidity_2m',
        'forecast_days': 3
    }
    
    response = requests.get(url, params=params)
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # Return None if the response is empty (though Open-Meteo usually returns data structure even if no hours)
    if not data:
        return None
        
    return data