import requests

def solve(inputs):
    """Delete a todo by identifier from DummyJSON and return isDeleted or None."""
    resource_id = inputs.get("resource_id")
    if resource_id is None:
        raise ValueError("Missing required input: resource_id")
    
    url = f"https://dummyjson.com/todos/{resource_id}"
    headers = {"Content-Type": "application/json"}
    payload = {}
    
    response = requests.delete(url, json=payload, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 200:
        return None
    
    data = response.json()
    is_deleted = data.get("isDeleted")
    return is_deleted