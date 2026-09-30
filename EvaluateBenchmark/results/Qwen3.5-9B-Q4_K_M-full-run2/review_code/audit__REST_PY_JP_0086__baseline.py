import requests

def solve(inputs):
    """
    Submits a new user to JSONPlaceholder using the provided name.
    
    Args:
        inputs (dict): A dictionary containing 'new_name' for the user's name.
        
    Returns:
        str or None: The response's 'name' value if present, otherwise None for a successful empty response.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    url = "https://jsonplaceholder.typicode.com/users"
    
    payload = {
        "name": inputs.get("new_name")
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create user. Status code: {response.status_code}")
    
    data = response.json()
    
    if "name" in data:
        return data["name"]
    else:
        return None