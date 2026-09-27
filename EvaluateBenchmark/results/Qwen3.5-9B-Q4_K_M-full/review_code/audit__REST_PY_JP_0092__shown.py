import requests

def solve(inputs):
    """Submit a new comment to JSONPlaceholder."""
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/comments"
    
    payload = {
        "email": inputs["new_email"],
        "name": inputs["new_name"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to submit comment. Status code: {response.status_code}")
    
    return response.json()