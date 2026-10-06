import requests

def solve(inputs):
    """
    Submit a new comment to JSONPlaceholder using the provided email and name.
    
    Args:
        inputs (dict): Dictionary containing:
            - new_email (str): The email value for the comment's 'email' attribute.
            - new_name (str): The name value for the comment's 'name' attribute.
    
    Returns:
        str or None: The 'name' value from the response, or None if absent or on empty response.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/comments"
    
    payload = {
        "email": inputs["new_email"],
        "name": inputs["new_name"]
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()  # Raise an exception for unsuccessful HTTP responses
    
    if response.status_code == 201:
        data = response.json()
        return data.get("name")
    elif response.status_code == 204:
        return None
    else:
        raise requests.exceptions.RequestException(f"Unexpected status code: {response.status_code}")