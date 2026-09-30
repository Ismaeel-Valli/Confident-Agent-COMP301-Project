import requests

def solve(inputs):
    """
    Submit a new user to JSONPlaceholder and return the response's name value,
    or None if that attribute is absent. Return None for a successful empty response.
    Raise an exception for an unsuccessful HTTP response.
    
    Args:
        inputs (dict): Dictionary containing 'new_name' key with the user's name.
        
    Returns:
        str or None: The name from the response, or None if absent or empty response.
        
    Raises:
        requests.RequestException: If the HTTP response is unsuccessful.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/users"
    
    payload = {
        "name": inputs["new_name"]
    }
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code >= 400:
            raise requests.RequestException(f"HTTP {response.status_code}: {response.text}")
        
        data = response.json()
        
        if isinstance(data, dict):
            return data.get("name")
        else:
            return None
            
    except requests.RequestException as e:
        raise