import requests

def solve(inputs):
    """
    Submits a new user to DummyJSON API using provided first name and username.
    
    Args:
        inputs (dict): Dictionary containing 'new_firstName' and 'new_username'.
        
    Returns:
        int or None: The ID of the created user, or None if response is empty.
        
    Raises:
        Exception: If HTTP response indicates failure.
    """
    url = "https://jsonplaceholder.typicode.com/users"
    
    payload = {
        "name": inputs.get("new_firstName"),
        "username": inputs.get("new_username")
    }
    
    # DummyJSON typically expects POST to /users with name and username
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create user. Status code: {response.status_code}")
    
    data = response.json()
    
    # Return id if present, otherwise None for empty/successful response without id
    return data.get("id")