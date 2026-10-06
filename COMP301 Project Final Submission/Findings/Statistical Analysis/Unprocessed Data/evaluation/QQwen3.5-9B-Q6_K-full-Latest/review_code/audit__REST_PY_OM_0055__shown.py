import requests

def solve(inputs):
    """
    Retrieve hourly cloud cover from Open-Meteo weather forecast service.
    
    Parameters:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    # Build the URL with parameters for 3 forecast days and hourly cloud cover
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'cloud_cover',
        'forecast_days': 3
    }
    
    url = "https://api.open-meteo.com/v1/forecast"
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (no data in hourly section)
    if not data.get('hourly') or len(data['hourly'].get('cloud_cover', [])) == 0:
        return None
    
    return data