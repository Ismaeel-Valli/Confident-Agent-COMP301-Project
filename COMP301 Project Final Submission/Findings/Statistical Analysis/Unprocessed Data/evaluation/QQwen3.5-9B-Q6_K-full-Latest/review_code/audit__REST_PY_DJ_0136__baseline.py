import requests
import json

def solve(inputs):
    """
    Submits a new user to DummyJSON API.
    
    Args:
        inputs (dict): Contains 'new_firstName' and 'new_username'.
        
    Returns:
        None if the response is successful and empty.
        The decoded JSON response otherwise.
        
    Raises:
        Exception for unsuccessful HTTP responses.
    """
    url = "https://dummyjson.com/users/addNewUser"
    
    payload = {
        "firstName": inputs["new_firstName"],
        "username": inputs["new_username"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to submit user. Status code: {response.status_code}, Response: {response.text}")
    
    return None