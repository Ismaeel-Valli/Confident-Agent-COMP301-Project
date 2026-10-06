import requests

def solve(inputs):
    """Retrieve a todo by identifier from DummyJSON and return its id."""
    resource_id = inputs["resource_id"]
    
    try:
        response = requests.get(f"https://dummyjson.com/todos/{resource_id}")
        
        if response.status_code != 200:
            raise Exception(f"HTTP error: {response.status_code} - {response.text}")
        
        data = response.json()
        
        # Check if the response is empty or lacks 'id'
        if not data or "id" not in data:
            return None
        
        return data["id"]
    
    except requests.RequestException as e:
        raise Exception(f"Request failed: {e}")