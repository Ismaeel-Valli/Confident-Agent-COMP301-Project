import requests

def solve(inputs):
    """
    Update a user in JSONPlaceholder.
    
    inputs: dict with keys:
        - resource_id: int, ID of the user to update
        - new_name: str, new name value
    
    Returns:
        - None if response is empty (successful)
        - Decoded JSON response otherwise
        - Raises exception on unsuccessful HTTP status
    """
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/users/{inputs['resource_id']}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "name": inputs["new_name"]
    }
    
    response = requests.put(url, json=payload, headers=headers)
    response.raise_for_status()
    
    if len(response.content) == 0:
        return None
    
    return response.json()