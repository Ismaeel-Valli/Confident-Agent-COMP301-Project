import requests

def solve(inputs):
    """
    Update a comment in JSONPlaceholder.
    
    inputs:
        resource_id (int): ID of the comment to update
        new_name (str): New value for the name attribute
    
    Returns:
        dict or None: Decoded JSON response, or None if empty
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://jsonplaceholder.typicode.com"
    resource_id = inputs["resource_id"]
    new_name = inputs["new_name"]
    
    url = f"{base_url}/comments/{resource_id}"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "name": new_name
    }
    
    response = requests.put(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 204:
        return None
    else:
        raise Exception(f"HTTP {response.status_code}: {response.text}")