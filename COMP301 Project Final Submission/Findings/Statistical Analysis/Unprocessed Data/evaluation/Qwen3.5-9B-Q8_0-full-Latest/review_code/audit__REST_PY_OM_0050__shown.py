import requests

def solve(inputs):
    """
    Retrieve hourly ozone from Open-Meteo air quality forecast service.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    base_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'ozone',
        'timezone': 'auto'
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (though unlikely for this API)
    if not data:
        return None
    
    return data