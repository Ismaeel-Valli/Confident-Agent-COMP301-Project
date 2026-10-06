import requests

def solve(inputs):
    """
    Retrieves hourly ozone data from Open-Meteo public API based on provided coordinates.
    
    Parameters:
        inputs (dict): A dictionary containing 'latitude' and 'longitude'.
        
    Returns:
        dict or None: The decoded JSON response if successful, or None if the response is empty.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "ozone",
        "timezone": "auto"
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
    
    if response.status_code == 204:
        return None
    
    try:
        data = response.json()
        return data
    except ValueError as e:
        raise requests.exceptions.JSONDecodeError(f"Failed to decode JSON response: {e}", response.text, response.content) from e