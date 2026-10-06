import requests

def solve(inputs):
    """
    Retrieve hourly wave direction from Open-Meteo marine forecast service.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    # Marine API endpoint for hourly wave data
    base_url = "https://marine-api.open-meteo.com/v1/marine"
    
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'wave_direction',
        'forecast_days': 3
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (no wave direction data)
    if not data.get('hourly', {}).get('wave_direction'):
        return None
    
    return data