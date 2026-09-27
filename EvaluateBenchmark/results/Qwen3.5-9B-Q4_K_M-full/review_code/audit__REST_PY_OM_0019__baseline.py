import requests

def solve(inputs):
    """
    Retrieves hourly relative humidity at two metres from the Open-Meteo public API
    for a given location, covering three forecast days.

    Args:
        inputs (dict): A dictionary containing 'latitude' and 'longitude'.

    Returns:
        dict or None: The decoded JSON response if data is present, None if the response is empty but successful.

    Raises:
        Exception: If the HTTP response is unsuccessful (status code not in 2xx range).
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']

    url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'relative_humidity_2m',
        'forecast_days': 3,
        'timezone': 'auto'
    }

    response = requests.get(url, params=params)

    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")

    data = response.json()

    # If the hourly data is empty (e.g., no valid forecast points), return None for a successful empty response.
    if not data.get('hourly', {}).get('relative_humidity_2m'):
        return None

    return data