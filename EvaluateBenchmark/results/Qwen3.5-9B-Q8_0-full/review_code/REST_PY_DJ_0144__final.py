import requests

def solve(inputs):
    """
    Update selected fields of a user on DummyJSON.
    
    Args:
        inputs (dict): Contains 'resource_id' (user ID) and 'new_username'.
        
    Returns:
        int or None: The response's id value, or None if absent or successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/users"
    resource_id = inputs["resource_id"]
    new_username = inputs["new_username"]
    
    url = f"{base_url}/{resource_id}"
    payload = {"username": new_username}
    
    response = requests.put(url, json=payload)
    
    if response.status_code >= 400:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Check for successful empty response (e.g., status 204 or similar with no content)
    if response.status_code == 204 or (data.get("status") == "success" and data.get("user") is None):
        return None
    
    # Return the id from the response
    user_data = data.get("user", {})
    return user_data.get("id")