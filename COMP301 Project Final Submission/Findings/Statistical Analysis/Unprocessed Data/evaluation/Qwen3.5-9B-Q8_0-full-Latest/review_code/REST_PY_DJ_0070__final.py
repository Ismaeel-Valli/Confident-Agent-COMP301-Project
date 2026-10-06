import requests

def solve(inputs):
    """Delete a post by identifier from DummyJSON and return isDeleted or None."""
    resource_id = inputs.get("resource_id")
    if resource_id is None:
        raise ValueError("Missing required input: resource_id")
    
    url = f"https://dummyjson.com/posts/{resource_id}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {"isDeleted": True}
    
    response = requests.delete(url, json=payload, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    
    if data.get("isDeleted") is not None:
        return data["isDeleted"]
    elif data == {}:
        return None
    else:
        return None