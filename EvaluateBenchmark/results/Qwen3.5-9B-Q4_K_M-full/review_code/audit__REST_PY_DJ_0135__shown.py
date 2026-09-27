import requests

def solve(inputs):
    """
    Update selected fields of a user in DummyJSON.
    
    Args:
        inputs (dict): Contains 'resource_id' and 'new_username'.
        
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/users"
    resource_id = inputs["resource_id"]
    new_username = inputs["new_username"]
    
    payload = {
        "username": new_username
    }
    
    response = requests.patch(
        f"{base_url}/{resource_id}",
        json=payload
    )
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 204:
        return None
    else:
        raise Exception(f"Failed to update user: {response.status_code} - {response.text}")