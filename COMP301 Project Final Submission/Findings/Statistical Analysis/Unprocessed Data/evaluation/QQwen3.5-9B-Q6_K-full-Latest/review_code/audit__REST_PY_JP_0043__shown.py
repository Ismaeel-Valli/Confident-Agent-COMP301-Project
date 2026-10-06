import requests

def solve(inputs):
    """Submit a new comment to JSONPlaceholder and return its id."""
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/comments"
    
    payload = {
        "name": inputs["new_name"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create comment: HTTP {response.status_code}")
    
    data = response.json()
    
    if "id" in data:
        return data["id"]
    elif data is None or (isinstance(data, dict) and len(data) == 0):
        return None
    else:
        return None