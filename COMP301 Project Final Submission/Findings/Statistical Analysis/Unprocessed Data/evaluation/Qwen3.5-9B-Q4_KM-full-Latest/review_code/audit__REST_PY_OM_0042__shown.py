def solve(inputs):
    import requests
    
    lat = inputs["latitude"]
    lon = inputs["longitude"]
    
    url = "https://marine-api.open-meteo.com/v1/marine"
    params = {
        "latitude": lat,
        "longitude": lon,
        "timezone": "auto"
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    return response.json()