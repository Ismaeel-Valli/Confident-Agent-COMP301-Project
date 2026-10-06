import requests

def solve(inputs):
    """
    Update an album in JSONPlaceholder with a new user identifier.
    
    Args:
        inputs (dict): Must contain 'resource_id' and 'new_user_identifier'.
        
    Returns:
        dict or None: The decoded JSON response, or None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    resource_id = inputs['resource_id']
    new_user_identifier = inputs['new_user_identifier']
    
    url = "https://jsonplaceholder.typicode.com/albums/" + str(resource_id)
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    payload = {
        "userId": new_user_identifier
    }
    
    response = requests.put(url, json=payload, headers=headers)
    
    if response.status_code >= 400:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    return response.json() if response.content else None