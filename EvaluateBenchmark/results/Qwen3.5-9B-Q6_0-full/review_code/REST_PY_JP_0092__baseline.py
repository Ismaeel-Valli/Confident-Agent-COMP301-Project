import requests

def solve(inputs):
    """
    Submits a new comment to JSONPlaceholder with updated email and name.
    
    Args:
        inputs (dict): Contains 'new_email' and 'new_name'.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty body.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    url = "https://jsonplaceholder.typicode.com/posts/1/comments"
    
    # Prepare the payload for the new comment
    payload = {
        "email": inputs["new_email"],
        "name": inputs["new_name"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 201:
        return None
    elif response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")