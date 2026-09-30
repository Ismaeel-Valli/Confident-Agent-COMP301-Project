import requests

def solve(inputs):
    """
    Retrieves hourly PM10 data from Open-Meteo Air Quality Forecast API.
    
    Args:
        inputs (dict): Must contain 'latitude' and 'longitude'.
        
    Returns:
        dict or None: Decoded JSON response. Returns None if the response is empty but successful.
        
    Raises:
        Exception: If the HTTP response is unsuccessful (status code outside 200-299).
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "pm10",
        "timezone": "auto"
    }
    
    response = requests.get(url, params=params)
    
    if not (200 <= response.status_code < 300):
        raise Exception(f"HTTP Error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Check if the hourly data is empty (e.g., no data points returned)
    if 'hourly' not in data or len(data['hourly']) == 0:
        return None
        
    return data