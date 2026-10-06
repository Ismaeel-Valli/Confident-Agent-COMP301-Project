import requests

def solve(inputs):
    """
    Submits a new comment to JSONPlaceholder with updated email and name.
    
    Args:
        inputs (dict): Contains 'new_email' and 'new_name'.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty body.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    url = "https://jsonplaceholder.typicode.com/posts/1/comments"
    
    # Prepare the payload for the new comment
    payload = {
        "email": inputs["new_email"],
        "name": inputs["new_name"]
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for unsuccessful HTTP responses
        
        if response.status_code == 201 or response.status_code == 200:
            return None  # Successful empty response as per requirement
        else:
            return response.json()
            
    except requests.RequestException as e:
        raise e