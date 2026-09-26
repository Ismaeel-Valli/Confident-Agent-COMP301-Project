```python
import requests

def solve(inputs):
    """
    Retrieves hourly temperature at two metres from the Open-Meteo public API.
    
    Args:
        inputs (dict): A dictionary containing 'latitude' and 'longitude'.
        
    Returns:
        dict or None: The decoded JSON response if data exists, or None for an empty successful response.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    latitude = inputs['latitude']
    longitude = inputs['longitude']
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
        "timezone": "auto"
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP Error {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for a successful empty response (e.g., no hourly data available)
    if not data.get("hourly"):
        return None
        
    return data
```