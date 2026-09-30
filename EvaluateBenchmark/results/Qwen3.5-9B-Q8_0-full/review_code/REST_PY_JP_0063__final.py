import requests

def solve(inputs):
    """Retrieve a user by identifier from JSONPlaceholder and return their id."""
    resource_id = inputs["resource_id"]
    
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/users", params={"id": resource_id})
        
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code} error")
        
        data = response.json()
        
        # Return id if present, None otherwise
        return data.get("id")
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")