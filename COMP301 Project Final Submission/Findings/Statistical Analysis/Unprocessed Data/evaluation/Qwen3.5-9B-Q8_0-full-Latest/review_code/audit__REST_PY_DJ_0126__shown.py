import requests

def solve(inputs):
    """
    Update selected fields of a user on DummyJSON.
    
    Args:
        inputs (dict): Contains 'resource_id' and 'new_phone'.
        
    Returns:
        int or None: The response's id value, or None if absent or successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/users"
    resource_id = inputs["resource_id"]
    new_phone = inputs["new_phone"]
    
    url = f"{base_url}/{resource_id}"
    payload = {"phone": new_phone}
    
    response = requests.put(url, json=payload)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return data.get("id")
    elif response.status_code == 204:
        return None
    else:
        raise Exception(f"Failed to update user. Status code: {response.status_code}")