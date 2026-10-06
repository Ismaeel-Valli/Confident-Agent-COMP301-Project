import requests

def solve(inputs):
    """
    Updates selected fields of a todo using DummyJSON API.
    
    Args:
        inputs (dict): Contains 'resource_id' (todo ID) and 'new_user_identifier' (new user ID).
        
    Returns:
        str or None: The response's 'id' value if present, otherwise None for successful empty responses.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    resource_id = inputs.get('resource_id')
    new_user_identifier = inputs.get('new_user_identifier')
    
    # Construct the update payload
    payload = {
        "user": new_user_identifier
    }
    
    # Endpoint for updating a todo (assuming standard REST pattern with DummyJSON)
    url = f"https://dummyjson.com/todos/{resource_id}"
    
    response = requests.put(url, json=payload)
    
    if response.status_code not in [200, 201]:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    # Check if the response is empty (no content)
    if not response.content:
        return None
    
    # Try to extract 'id' from the JSON response
    try:
        data = response.json()
        return data.get('id')
    except ValueError:
        # If response is not valid JSON but status was 200/201, treat as empty success
        return None