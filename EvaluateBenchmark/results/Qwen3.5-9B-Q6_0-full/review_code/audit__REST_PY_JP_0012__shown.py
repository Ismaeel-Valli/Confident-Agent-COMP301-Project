import requests


def solve(inputs):
    """Delete a comment by identifier from JSONPlaceholder."""
    resource_id = inputs["resource_id"]
    url = f"https://jsonplaceholder.typicode.com/comments/{resource_id}"
    
    response = requests.delete(url)
    
    if response.status_code == 204:
        return None
    
    response.raise_for_status()
    return response.json()