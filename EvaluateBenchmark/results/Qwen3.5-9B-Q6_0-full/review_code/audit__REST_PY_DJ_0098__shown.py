import requests

def solve(inputs):
    """
    Submit a new user to DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - new_email (str): Email for the new user
            - new_firstName (str): First name for the new user
    
    Returns:
        dict: Decoded JSON response, or None if successful with empty response
        Raises: Exception on unsuccessful HTTP response
    """
    base_url = "https://dummyjson.com/users/add"
    
    payload = {
        "email": inputs["new_email"],
        "firstName": inputs["new_firstName"]
    }
    
    try:
        response = requests.post(base_url, json=payload)
        
        if response.status_code == 201:
            # Successful creation - return decoded JSON or None for empty response
            data = response.json()
            return data if data else None
        elif response.status_code in [400, 409]:
            # Bad request or conflict - raise exception
            response.raise_for_status()
        else:
            # Other unsuccessful status codes
            response.raise_for_status()
            
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Failed to create user: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")