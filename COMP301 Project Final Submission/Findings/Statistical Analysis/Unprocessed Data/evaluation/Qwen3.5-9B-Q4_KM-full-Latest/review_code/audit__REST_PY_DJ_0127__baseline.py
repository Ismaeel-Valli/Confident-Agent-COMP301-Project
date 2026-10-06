import requests

def solve(inputs):
    """
    Submits a new user to DummyJSON API using provided first name and phone number.
    
    Args:
        inputs (dict): Dictionary containing 'new_firstName' and 'new_phone'.
        
    Returns:
        str or None: The response's 'id' value if present, otherwise None for successful empty response.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    url = "https://dummyjson.com/users"
    
    payload = {
        "firstName": inputs.get("new_firstName"),
        "phone": inputs.get("new_phone")
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create user. Status code: {response.status_code}, Response: {response.text}")
    
    data = response.json()
    
    # DummyJSON returns the created user in 'user' key for POST requests
    if "user" in data and "id" in data["user"]:
        return data["user"]["id"]
    elif not data or (isinstance(data, dict) and len(data) == 0):
        return None
    else:
        # If response is successful but no 'id' found in expected structure
        return None