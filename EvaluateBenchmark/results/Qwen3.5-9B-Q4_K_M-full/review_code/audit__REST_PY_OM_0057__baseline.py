import requests

def solve(inputs):
    """
    Retrieves hourly swell wave height from the Open-Meteo marine forecast service.
    
    Args:
        inputs (dict): A dictionary containing 'latitude' and 'longitude'.
        
    Returns:
        dict or None: The decoded JSON response if data exists, or None for an empty successful response.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    # Construct the URL with parameters for swell height and 3 days of forecast
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "swell_height",
        "forecast_days": 3
    }
    
    response = requests.get(url, params=params)
    
    # Raise an exception for unsuccessful HTTP responses
    if response.status_code != 200:
        raise Exception(f"HTTP request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for a successful empty response (e.g., no hourly swell_height data)
    if not data.get("hourly", {}).get("swell_height"):
        return None
        
    return data