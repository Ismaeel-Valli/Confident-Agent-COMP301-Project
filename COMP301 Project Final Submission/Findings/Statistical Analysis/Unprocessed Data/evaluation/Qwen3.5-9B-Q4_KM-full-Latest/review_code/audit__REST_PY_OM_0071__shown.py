import requests

def solve(inputs):
    """
    Retrieve hourly PM10 and PM2.5 from Open-Meteo air quality forecast service.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    lat = inputs['latitude']
    lon = inputs['longitude']
    
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "pm10,pm2_5",
        "timezone": "auto",
        "forecast_days": 3
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    return response.json()