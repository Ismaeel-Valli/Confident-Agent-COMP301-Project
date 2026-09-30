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
    
    payload = {
        "phone": new_phone
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code not in [200, 201]:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Check for id in the response
    if "id" in data and data["id"] is not None:
        return data["id"]
    
    # Return None for successful empty response or missing id
    return None