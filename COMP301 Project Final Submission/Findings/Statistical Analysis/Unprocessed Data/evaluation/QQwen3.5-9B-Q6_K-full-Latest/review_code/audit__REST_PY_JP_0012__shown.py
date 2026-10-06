import requests

def solve(inputs):
    """Delete a comment by identifier from JSONPlaceholder."""
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/comments/{inputs['resource_id']}"
    
    response = requests.delete(url)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    return response.json()