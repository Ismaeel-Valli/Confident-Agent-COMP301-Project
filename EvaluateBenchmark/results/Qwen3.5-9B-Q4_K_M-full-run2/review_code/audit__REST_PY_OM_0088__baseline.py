import requests

def solve(inputs):
    """
    Retrieves hourly temperature at two metres and wind speed at ten metres 
    from the Open-Meteo public API for a given location.
    
    Args:
        inputs (dict): A dictionary containing 'latitude' and 'longitude'.
        
    Returns:
        dict or None: The decoded JSON response, or None if the response is empty.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    # Construct the API URL with parameters for hourly temperature and wind speed
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'temperature_2m,wind_speed_10m',
        'timezone': 'auto'  # Automatically determine the time zone
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP request failed with status code {response.status_code}")
    
    data = response.json()
    
    # Return None for a successful empty response
    if not data:
        return None
    
    return data