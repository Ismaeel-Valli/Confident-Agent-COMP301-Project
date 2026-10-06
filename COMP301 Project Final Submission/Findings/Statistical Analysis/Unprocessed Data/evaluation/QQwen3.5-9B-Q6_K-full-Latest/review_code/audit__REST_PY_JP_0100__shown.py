import requests

def solve(inputs):
    """
    Submit a new user to JSONPlaceholder.
    
    Args:
        inputs (dict): Must contain 'new_name' and 'new_username'.
        
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/users"
    
    payload = {
        "name": inputs["new_name"],
        "username": inputs["new_username"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 201:
        return None
    
    elif response.status_code == 200:
        return response.json()
    
    else:
        raise Exception(f"Failed to create user. Status code: {response.status_code}")