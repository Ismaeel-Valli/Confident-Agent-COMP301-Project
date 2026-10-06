import requests

def solve(inputs):
    """Retrieve a photo by identifier from JSONPlaceholder and return its title."""
    resource_id = inputs["resource_id"]
    
    url = "https://jsonplaceholder.typicode.com/photos"
    params = {"id": resource_id}
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    data = response.json()
    
    if data is None or "title" not in data:
        return None
    
    return data["title"]