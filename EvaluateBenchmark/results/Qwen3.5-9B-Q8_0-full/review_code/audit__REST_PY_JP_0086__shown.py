import requests

def solve(inputs):
    """
    Submit a new user to JSONPlaceholder and return the name value from the response.
    
    Args:
        inputs (dict): Dictionary containing 'new_name' for the user's name.
        
    Returns:
        str or None: The name value from the response, or None if absent or empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/users"
    
    payload = {
        "name": inputs["new_name"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create user. Status code: {response.status_code}")
    
    data = response.json()
    
    if "name" not in data or not data["name"]:
        return None
    
    return data["name"]