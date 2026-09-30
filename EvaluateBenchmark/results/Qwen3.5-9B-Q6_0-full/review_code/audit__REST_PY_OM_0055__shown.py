import requests

def solve(inputs):
    """
    Retrieve hourly cloud cover from Open-Meteo weather forecast service for three days.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    # Build URL with parameters for 3 days of hourly forecast and cloud cover
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'cloud_cover',
        'forecast_days': 3
    }
    
    url = "https://api.open-meteo.com/v1/forecast"
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    # Return None for successful empty response (though unlikely with this API)
    if not data:
        return None
    
    return data