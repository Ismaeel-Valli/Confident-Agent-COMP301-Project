import requests

def solve(inputs):
    """
    Retrieves hourly relative humidity at two metres from Open-Meteo public API
    for a given location covering three forecast days.

    Args:
        inputs (dict): A dictionary containing 'latitude' and 'longitude'.

    Returns:
        dict or None: The decoded JSON response if successful, or None if the response is empty.

    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "relative_humidity_2m",
        "forecast_days": 3
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")

    return response.json() if response.json() else None