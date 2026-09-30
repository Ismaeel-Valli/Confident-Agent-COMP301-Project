import requests

def solve(inputs):
    """Delete a user by identifier from DummyJSON and return isDeleted value."""
    resource_id = inputs["resource_id"]
    
    url = f"https://dummyjson.com/users/{resource_id}"
    headers = {"Content-Type": "application/json"}
    payload = {}
    
    response = requests.delete(url, json=payload, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return None
    
    result = response.json()
    is_deleted = result.get("isDeleted")
    return is_deleted