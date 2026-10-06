import requests

def solve(inputs):
    """
    Retrieves hourly swell wave height from Open-Meteo marine forecast service.
    
    Args:
        inputs (dict): Dictionary containing 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response, or None if the response is empty but successful.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    # Construct the URL for the marine forecast service
    url = "https://api.open-meteo.com/v1/forecast"
    
    # Define parameters
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'swellHeight',
        'timezone': 'auto',
        'forecast_days': 3
    }
    
    # Send the GET request
    response = requests.get(url, params=params)
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # Return None if the response is empty (though this is unlikely given the API structure)
    if not data:
        return None
    
    return data