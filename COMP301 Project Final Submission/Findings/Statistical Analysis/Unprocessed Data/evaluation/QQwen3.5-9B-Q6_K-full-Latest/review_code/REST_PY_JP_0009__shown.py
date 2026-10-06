import requests

def solve(inputs):
    """Retrieve a comment by identifier from JSONPlaceholder."""
    resource_id = inputs["resource_id"]
    
    url = "https://jsonplaceholder.typicode.com/comments"
    params = {"postId": resource_id}
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return None if len(data) == 0 else data[0]
    else:
        raise Exception(f"HTTP error {response.status_code}: {response.text}")