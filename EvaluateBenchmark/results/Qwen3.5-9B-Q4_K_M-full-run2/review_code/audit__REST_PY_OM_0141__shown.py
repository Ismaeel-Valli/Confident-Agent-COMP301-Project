import requests

def solve(inputs):
    """
    Retrieve hourly wave direction and swell wave height from Open-Meteo marine forecast service.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    lat = inputs['latitude']
    lon = inputs['longitude']
    
    base_url = "https://marine-api.open-meteo.com/v1/marine"
    url = f"{base_url}?latitude={lat}&longitude={lon}&hourly=wave_direction,swell_wave_height&forecast_days=3"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    return response.json()