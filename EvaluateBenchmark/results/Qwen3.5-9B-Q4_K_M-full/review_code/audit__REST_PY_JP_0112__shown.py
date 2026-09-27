import requests

def solve(inputs):
    """
    Submit a new user to JSONPlaceholder and return the response's id value,
    or None if that attribute is absent. Return None for a successful empty response.
    Raise an exception for an unsuccessful HTTP response.
    
    Args:
        inputs (dict): Dictionary containing:
            - new_name (str): Value for the name attribute
            - new_username (str): Value for the username attribute
    
    Returns:
        int or None: The id of the created user, or None if absent or empty response
    
    Raises:
        requests.RequestException: For unsuccessful HTTP responses
    """
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/users"
    
    payload = {
        "name": inputs["new_name"],
        "username": inputs["new_username"]
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    if response.status_code == 201:
        data = response.json()
        return data.get("id")
    elif response.status_code == 204:
        return None
    else:
        raise requests.RequestException(f"Failed to create user: {response.status_code} {response.text}")