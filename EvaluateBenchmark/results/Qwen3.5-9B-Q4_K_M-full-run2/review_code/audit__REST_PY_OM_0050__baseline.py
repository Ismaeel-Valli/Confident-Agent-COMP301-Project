import requests

def solve(inputs):
    """
    Retrieves hourly ozone data from the Open-Meteo public API's air quality forecast service.
    
    Args:
        inputs (dict): A dictionary containing 'latitude' and 'longitude'.
        
    Returns:
        dict or None: The decoded JSON response if successful. Returns None for an empty response.
        
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not in 2xx range).
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "o3",
        "timezone": "auto"
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for a successful empty response (e.g., no hourly ozone data available)
    if not data or 'hourly' not in data:
        return None
        
    return data