import requests

def solve(inputs):
    """Retrieve a comment by identifier from JSONPlaceholder and return its name."""
    resource_id = inputs["resource_id"]
    
    url = "https://jsonplaceholder.typicode.com/comments"
    params = {"postId": resource_id}
    
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise exception for unsuccessful HTTP responses
    
    data = response.json()
    
    if not data:
        return None
    
    comment = data[0]
    name = comment.get("name")
    
    return name