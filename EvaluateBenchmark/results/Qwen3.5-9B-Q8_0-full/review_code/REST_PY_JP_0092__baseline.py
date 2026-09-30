import requests

def solve(inputs):
    """
    Submits a new comment to JSONPlaceholder with updated email and name.
    
    Args:
        inputs (dict): Dictionary containing:
            - new_email (str): Value for the email attribute
            - new_name (str): Value for the name attribute
    
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response
    
    Raises:
        requests.RequestException: If HTTP response is unsuccessful
    """
    url = "https://jsonplaceholder.typicode.com/posts/1/comments"
    
    payload = {
        "email": inputs["new_email"],
        "name": inputs["new_name"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise requests.RequestException(f"Failed to submit comment: {response.status_code} - {response.text}")
    
    return None