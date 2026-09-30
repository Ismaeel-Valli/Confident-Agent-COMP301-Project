import requests

def solve(inputs):
    """
    Submits a new user to JSONPlaceholder API.
    
    Args:
        inputs (dict): Dictionary containing 'new_name' and 'new_username'.
        
    Returns:
        str or None: The name value from the response, or None if successful with empty response.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    url = "https://jsonplaceholder.typicode.com/users"
    
    payload = {
        "name": inputs["new_name"],
        "username": inputs["new_username"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create user. Status code: {response.status_code}")
        
    data = response.json()
    
    if not data:
        return None
        
    return data.get("name")