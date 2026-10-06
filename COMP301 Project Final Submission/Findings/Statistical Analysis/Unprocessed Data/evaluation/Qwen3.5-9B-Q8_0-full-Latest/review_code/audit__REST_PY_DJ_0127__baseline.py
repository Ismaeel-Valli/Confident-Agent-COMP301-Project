import requests

def solve(inputs):
    """
    Submits a new user to DummyJSON API using provided first name and phone number.
    
    Args:
        inputs (dict): Dictionary containing 'new_firstName' and 'new_phone'.
        
    Returns:
        int or None: The ID of the created user, or None if response is empty/missing ID.
        
    Raises:
        requests.exceptions.RequestException: If HTTP request fails.
    """
    url = "https://dummyjson.com/users/add"
    
    payload = {
        "firstName": inputs.get("new_firstName"),
        "phone": inputs.get("new_phone")
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to create user. Status code: {response.status_code}, Response: {response.text}")
    
    data = response.json()
    
    # Check for successful empty response (no content or empty dict)
    if not data or "id" not in data:
        return None
    
    return data.get("id")