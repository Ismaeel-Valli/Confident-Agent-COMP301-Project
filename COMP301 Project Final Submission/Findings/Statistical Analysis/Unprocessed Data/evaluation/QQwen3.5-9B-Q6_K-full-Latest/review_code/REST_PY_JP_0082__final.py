import requests

def solve(inputs):
    """Submit a new todo to JSONPlaceholder and return its title."""
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/todos"
    
    payload = {
        "title": inputs["new_title"],
        "body": "",
        "userId": 1
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    if response.status_code == 201:
        data = response.json()
        return data.get("title")
    elif response.status_code == 200:
        # Empty response or no title field
        return None
    else:
        raise Exception(f"Failed to create todo: HTTP {response.status_code}")