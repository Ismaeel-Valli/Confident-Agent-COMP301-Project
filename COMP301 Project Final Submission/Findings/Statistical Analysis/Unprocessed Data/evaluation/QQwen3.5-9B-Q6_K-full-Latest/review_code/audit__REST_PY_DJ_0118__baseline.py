import requests
import json

def solve(inputs):
    """
    Submits a new user to DummyJSON API using provided inputs.
    
    Args:
        inputs (dict): Dictionary containing 'new_firstName' and 'new_phone'.
        
    Returns:
        None if the response is empty (successful).
        Decoded JSON response otherwise.
        
    Raises:
        Exception for unsuccessful HTTP responses.
    """
    url = "https://dummyjson.com/users/addNewUser"
    
    # Prepare the payload with required fields
    payload = {
        "firstName": inputs.get("new_firstName"),
        "phone": inputs.get("new_phone")
    }
    
    try:
        response = requests.post(url, json=payload)
        
        # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
        response.raise_for_status()
        
        # Decode the JSON response
        decoded_response = response.json()
        
        # Return None if the response is empty (successful case as per requirement)
        if not decoded_response:
            return None
            
        return decoded_response
        
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")