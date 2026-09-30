import requests

def solve(inputs):
    """
    Retrieve hourly PM10 from Open-Meteo air quality forecast service.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    lat = inputs['latitude']
    lon = inputs['longitude']
    
    base_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    url = f"{base_url}?latitude={lat}&longitude={lon}&hourly=pm10"
    
    response = requests.get(url)
    response.raise_for_status()
    
    return response.json()