import requests

def solve(inputs):
    """Retrieve a post by identifier from JSONPlaceholder."""
    resource_id = inputs["resource_id"]
    
    url = "https://jsonplaceholder.typicode.com/posts"
    params = {"id": resource_id}
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    if not data:
        return None
    
    return data