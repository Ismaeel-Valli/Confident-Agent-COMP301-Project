import requests

def solve(inputs):
    """
    Update selected fields of a todo on DummyJSON.
    
    Args:
        inputs (dict): Contains 'resource_id' and 'new_user_identifier'.
        
    Returns:
        int or None: The response's id value, or None if absent or successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com"
    resource_id = inputs["resource_id"]
    new_user_identifier = inputs["new_user_identifier"]
    
    url = f"{base_url}/todos/{resource_id}"
    
    payload = {
        "userId": new_user_identifier
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code not in [200, 201, 204]:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    if response.status_code == 204:
        return None
    
    data = response.json()
    
    if "id" in data:
        return data["id"]
    
    return None