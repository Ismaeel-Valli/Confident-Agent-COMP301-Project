import requests

def solve(inputs):
    """
    Update selected fields of a post on DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - resource_id (int): Identifier of the post to update.
            - new_user_identifier (str): New value for the 'user' field.
    
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response.
    
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    base_url = "https://dummyjson.com/posts"
    resource_id = inputs["resource_id"]
    new_user_identifier = inputs["new_user_identifier"]
    
    url = f"{base_url}/{resource_id}"
    
    payload = {
        "user": new_user_identifier
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.put(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return None
    elif response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"HTTP {response.status_code}: {response.text}")