import requests

def solve(inputs):
    """Retrieve a comment by identifier from JSONPlaceholder."""
    resource_id = inputs["resource_id"]
    url = "https://jsonplaceholder.typicode.com/comments"
    
    response = requests.get(url, params={"postId": resource_id})
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data