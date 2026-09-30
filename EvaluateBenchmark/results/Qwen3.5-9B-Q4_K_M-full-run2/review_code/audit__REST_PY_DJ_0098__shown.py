import requests

def solve(inputs):
    """
    Submit a new user to DummyJSON using the provided email and first name.
    
    Args:
        inputs (dict): Must contain 'new_email' and 'new_firstName'.
        
    Returns:
        dict or None: The decoded JSON response, or None if the response is empty.
        
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not in 2xx).
    """
    base_url = "https://dummyjson.com/users/add"
    
    payload = {
        "email": inputs["new_email"],
        "firstName": inputs["new_firstName"]
    }
    
    response = requests.post(base_url, json=payload)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")
    
    return response.json() if response.content else None