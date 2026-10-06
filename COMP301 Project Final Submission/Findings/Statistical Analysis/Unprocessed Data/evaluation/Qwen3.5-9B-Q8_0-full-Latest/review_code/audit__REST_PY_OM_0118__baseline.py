import requests

def solve(inputs):
    """
    Retrieves hourly relative humidity at two metres and precipitation 
    from the Open-Meteo public API for a given location over three forecast days.
    
    Args:
        inputs (dict): A dictionary containing 'latitude' and 'longitude'.
        
    Returns:
        dict or None: The decoded JSON response if successful, or None if the response is empty.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    # Construct the API URL with parameters for 3 days of forecast (72 hours)
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'relative_humidity_2m,precipitation',
        'timezone': 'auto',
        'forecast_days': 3
    }
    
    url = "https://api.open-meteo.com/v1/forecast"
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        # Return None if the response is empty (though unlikely with this API structure)
        if not data:
            return None
            
        return data
        
    except requests.RequestException as e:
        raise e