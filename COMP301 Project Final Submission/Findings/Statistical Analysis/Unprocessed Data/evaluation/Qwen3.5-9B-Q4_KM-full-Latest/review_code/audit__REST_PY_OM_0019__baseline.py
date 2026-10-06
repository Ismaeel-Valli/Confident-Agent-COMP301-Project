import requests

def solve(inputs):
    """
    Retrieves hourly relative humidity at two metres from the Open-Meteo public API
    for a given location, covering three forecast days.

    Args:
        inputs (dict): A dictionary containing 'latitude' and 'longitude'.

    Returns:
        dict or None: The decoded JSON response if data is present, or None if the response is empty but successful.

    Raises:
        Exception: If the HTTP request fails (non-successful status code).
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']

    # Construct the API URL with parameters for 3 days of forecast and specific variable
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'relative_humidity_2m',
        'forecast_days': 3
    }

    url = "https://api.open-meteo.com/v1/forecast"

    try:
        response = requests.get(url, params=params)
        
        # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
        response.raise_for_status()
        
        # Decode the JSON response
        data = response.json()
        
        # Return None if the hourly data list is empty, otherwise return the decoded JSON
        if not data.get('hourly', {}).get('relative_humidity_2m'):
            return None
            
        return data

    except requests.exceptions.HTTPError as http_err:
        raise Exception(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        raise Exception(f"Request failed: {req_err}")