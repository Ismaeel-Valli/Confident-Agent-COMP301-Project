import requests

def solve(inputs):
    """Retrieve a todo by identifier from JSONPlaceholder and return its title."""
    resource_id = inputs["resource_id"]
    
    try:
        response = requests.get(f"https://jsonplaceholder.typicode.com/todos/{resource_id}")
        response.raise_for_status()
        
        if response.status_code == 200:
            data = response.json()
            return data.get("title")
        else:
            return None
            
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")