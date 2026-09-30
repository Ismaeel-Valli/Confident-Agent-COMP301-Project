import requests

def solve(inputs):
    """
    Retrieves hourly temperature at two metres and precipitation from Open-Meteo API.
    
    Args:
        inputs (dict): A dictionary containing 'latitude' and 'longitude'.
        
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation",
        "timezone": "auto"
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Check if the hourly data is empty (though unlikely with valid coords)
    if not data.get("hourly"):
        return None
        
    return data