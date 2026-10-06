import requests

def solve(inputs):
    """
    Update a comment's email field in JSONPlaceholder.
    
    Parameters:
        inputs (dict): Must contain 'resource_id' and 'new_email'.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty body.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    resource_id = inputs["resource_id"]
    new_email = inputs["new_email"]
    
    url = f"https://jsonplaceholder.typicode.com/comments/{resource_id}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "email": new_email
    }
    
    response = requests.put(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return None
    elif response.status_code == 204:
        return None
    else:
        response.raise_for_status()