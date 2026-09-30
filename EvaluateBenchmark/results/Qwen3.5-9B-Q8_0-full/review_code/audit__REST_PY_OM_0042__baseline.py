import requests

def solve(inputs):
    """
    Retrieves hourly wind wave height from the Open-Meteo marine forecast service.
    
    Args:
        inputs (dict): A dictionary containing 'latitude' and 'longitude'.
        
    Returns:
        dict or None: The decoded JSON response, or None if the response is successful but empty.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    # Construct the URL for the marine forecast service
    url = "https://api.open-meteo.com/v1/forecast"
    
    # Define parameters
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'windSpeed,waveHeight',
        'timezone': 'auto'  # Automatically determine the time zone
    }
    
    # Send the GET request
    response = requests.get(url, params=params)
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # Return None if the response is successful but empty (though unlikely for this API)
    if not data:
        return None
    
    return data