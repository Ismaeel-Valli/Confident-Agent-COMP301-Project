import requests

def solve(inputs):
    """
    Submits a new photo to JSONPlaceholder using the provided inputs dictionary.
    
    Args:
        inputs (dict): Must contain 'new_title' for the title attribute.
        
    Returns:
        str: The response's title value if present, or None if absent or response is empty.
        
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not in 2xx range).
        
    Note: Assumes referenced resources and accounts exist.
    """
    url = "https://jsonplaceholder.typicode.com/photos"
    
    # Prepare the payload using 'new_title' from inputs
    payload = {
        "title": inputs.get("new_title")
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses
    if not response.ok:
        raise Exception(f"HTTP request failed with status code: {response.status_code}")
    
    # Return the title value from the response if present, otherwise None
    return response.json().get("title")