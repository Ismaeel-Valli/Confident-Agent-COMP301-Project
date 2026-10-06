import requests

def solve(inputs):
    """
    Retrieves hourly precipitation and wind speed at ten metres from Open-Meteo API.
    
    Args:
        inputs (dict): A dictionary containing 'latitude' and 'longitude'.
        
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "precipitation,windspeed_10m",
        "timezone": "auto"
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
    
    data = response.json()
    
    # Check if the hourly data is empty
    if not data.get("hourly"):
        return None
        
    return data