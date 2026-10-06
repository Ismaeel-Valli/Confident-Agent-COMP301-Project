import requests

def solve(inputs):
    """
    Updates the 'name' field of a user on JSONPlaceholder and returns the new name.
    
    Args:
        inputs (dict): Must contain 'resource_id' (user ID) and 'new_name'.
        
    Returns:
        str or None: The updated name if present in response, otherwise None for success.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    resource_id = inputs['resource_id']
    new_name = inputs['new_name']
    
    url = f"https://jsonplaceholder.typicode.com/users/{resource_id}"
    payload = {"name": new_name}
    
    response = requests.put(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update user: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return the name if present in the response, otherwise None for a successful empty response
    return data.get("name")