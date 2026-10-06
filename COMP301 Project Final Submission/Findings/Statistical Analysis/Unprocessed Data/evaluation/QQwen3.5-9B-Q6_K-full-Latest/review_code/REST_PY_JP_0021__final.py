import requests

def solve(inputs):
    """Retrieve a photo by identifier from JSONPlaceholder."""
    resource_id = inputs["resource_id"]
    url = "https://jsonplaceholder.typicode.com/photos"
    
    response = requests.get(url, params={"id": resource_id})
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return None if data is None else data
    
    raise Exception(f"Unsuccessful HTTP response: {response.status_code}")