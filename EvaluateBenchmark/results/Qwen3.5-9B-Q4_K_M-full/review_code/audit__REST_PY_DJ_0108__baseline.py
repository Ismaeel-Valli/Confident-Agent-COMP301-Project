import requests

def solve(inputs):
    """
    Submits a new user to DummyJSON using the provided email and first name.
    
    Args:
        inputs (dict): A dictionary containing 'new_email' and 'new_firstName'.
        
    Returns:
        int or None: The ID of the created user, or None if the response is empty/successful without an ID.
        
    Raises:
        Exception: If the HTTP response indicates an error (non-2xx status code).
    """
    url = "https://jsonplaceholder.typicode.com/users"
    
    payload = {
        "email": inputs.get("new_email"),
        "firstName": inputs.get("new_firstName")
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Failed to create user. HTTP Status Code: {response.status_code}")
    
    # DummyJSON typically returns the created object with an 'id' field upon success
    data = response.json()
    
    if "id" in data:
        return data["id"]
    else:
        return None