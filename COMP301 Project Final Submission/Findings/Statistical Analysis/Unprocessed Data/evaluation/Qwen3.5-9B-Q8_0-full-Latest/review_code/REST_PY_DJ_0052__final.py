import requests

def solve(inputs):
    """
    Submit a new user to DummyJSON using the provided first and last name.
    
    Args:
        inputs (dict): Dictionary containing 'new_firstName' and 'new_lastName'.
        
    Returns:
        dict or None: Decoded JSON response, or None if response is empty.
        
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    base_url = "https://dummyjson.com/users/add"
    
    payload = {
        "firstName": inputs["new_firstName"],
        "lastName": inputs["new_lastName"]
    }
    
    try:
        response = requests.post(base_url, json=payload)
        
        if response.status_code == 201:
            data = response.json()
            return data.get("user") if data else None
        elif response.status_code == 200:
            data = response.json()
            return data.get("user") if data else None
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")