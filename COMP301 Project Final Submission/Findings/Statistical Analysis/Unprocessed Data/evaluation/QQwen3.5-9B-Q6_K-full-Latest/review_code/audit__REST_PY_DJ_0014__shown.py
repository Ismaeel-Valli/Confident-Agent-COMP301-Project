import requests

def solve(inputs):
    """Retrieve a post by identifier from DummyJSON."""
    resource_id = inputs["resource_id"]
    url = f"https://dummyjson.com/posts/{resource_id}"
    
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for unsuccessful HTTP responses
    
    if response.status_code == 204:
        return None
    
    return response.json()