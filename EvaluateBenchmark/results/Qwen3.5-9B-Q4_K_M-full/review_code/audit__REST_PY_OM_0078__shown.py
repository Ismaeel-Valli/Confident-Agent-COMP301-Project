import requests

def solve(inputs):
    """
    Retrieve hourly wave height and period from Open-Meteo marine forecast service.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
        
    Raises:
        requests.RequestException: For unsuccessful HTTP responses.
    """
    lat = inputs['latitude']
    lon = inputs['longitude']
    
    url = "https://marine-api.open-meteo.com/v1/marine"
    params = {
        'latitude': lat,
        'longitude': lon,
        'timezone': 'auto'
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    return response.json()