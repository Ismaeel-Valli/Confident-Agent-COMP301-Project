import requests

def solve(inputs):
    """
    Retrieve hourly fine particulate matter (PM2.5) from Open-Meteo air quality forecast service.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    lat = inputs['latitude']
    lon = inputs['longitude']
    
    # Open-Meteo air quality API endpoint for hourly PM2.5 forecast (3 days)
    base_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        'latitude': lat,
        'longitude': lon,
        'hourly': 'pm2_5',
        'forecast_days': 3
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (no forecast data)
    if not data.get('hourly'):
        return None
    
    return data