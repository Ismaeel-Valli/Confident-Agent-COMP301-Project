import requests

def solve(inputs):
    """
    Retrieve hourly precipitation from Open-Meteo weather forecast service.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    # Build URL with parameters for 3 days of hourly precipitation forecast
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'precipitation',
        'forecast_days': 3
    }
    
    url = "https://api.open-meteo.com/v1/forecast"
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (though forecast won't be empty)
    if not data:
        return None
    
    return data