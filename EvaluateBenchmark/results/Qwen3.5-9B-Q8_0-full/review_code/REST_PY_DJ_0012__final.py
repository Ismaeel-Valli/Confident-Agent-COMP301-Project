import requests
import json

def solve(inputs):
    """
    Submit a new user to DummyJSON using the provided first name.
    
    Args:
        inputs (dict): Must contain 'new_firstName' key with the user's first name.
        
    Returns:
        dict or None: The decoded JSON response if successful, None for empty response.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://dummyjson.com/users/add"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "firstName": inputs["new_firstName"]
    }
    
    try:
        response = requests.post(base_url, json=payload, headers=headers)
        
        if response.status_code == 201:
            data = response.json()
            return data.get("user") if data else None
        elif response.status_code == 200:
            data = response.json()
            return data.get("user") if data else None
        else:
            raise Exception(f"Failed to create user. Status code: {response.status_code}, Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")