import requests

def solve(inputs):
    """
    Submits a new user to DummyJSON API with provided first name and phone number.
    
    Args:
        inputs (dict): Dictionary containing 'new_firstName' and 'new_phone'.
        
    Returns:
        int or None: The ID of the created user, or None if response is empty.
        
    Raises:
        requests.exceptions.RequestException: If HTTP request fails.
    """
    url = "https://dummyjson.com/users/add"
    
    payload = {
        "firstName": inputs["new_firstName"],
        "phone": inputs["new_phone"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to create user. Status code: {response.status_code}")
    
    data = response.json()
    
    # Check for empty response (no users array or empty array)
    if not data.get("users") or len(data["users"]) == 0:
        return None
    
    # Return the ID of the newly created user
    return data["users"][0]["id"]