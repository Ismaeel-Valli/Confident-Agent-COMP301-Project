import requests

def solve(inputs):
    """
    Update selected fields of a user on DummyJSON.
    
    Args:
        inputs (dict): Contains 'resource_id' (user ID) and 'new_phone' (phone value).
        
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com"
    resource_id = inputs["resource_id"]
    new_phone = inputs["new_phone"]
    
    url = f"{base_url}/users/{resource_id}"
    
    payload = {
        "phone": new_phone
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code >= 400:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    return response.json() if response.content else None