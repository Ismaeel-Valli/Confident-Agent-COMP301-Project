import requests

def solve(inputs):
    """
    Retrieve hourly relative humidity at two metres and precipitation from Open-Meteo,
    covering three forecast days. Returns decoded JSON response (None for empty) or
    raises an exception on HTTP error.
    
    Inputs:
        inputs['latitude']: float
        inputs['longitude']: float
    
    Returns:
        dict or None (decoded JSON)
    
    Raises:
        requests.RequestException on unsuccessful HTTP response
    """
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": inputs["latitude"],
        "longitude": inputs["longitude"],
        "hourly": "relative_humidity_2m,precipitation",
        "forecast_days": 3
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    return response.json()