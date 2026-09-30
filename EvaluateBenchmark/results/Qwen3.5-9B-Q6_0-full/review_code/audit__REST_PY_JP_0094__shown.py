import requests

def solve(inputs):
    """
    Submit a new album to JSONPlaceholder.
    
    Args:
        inputs (dict): Must contain:
            - 'new_title': str, the title for the album
            - 'new_user_identifier': int or str, the user ID
    
    Returns:
        dict or None: The decoded JSON response if successful; None for empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    url = "https://jsonplaceholder.typicode.com/albums"
    title = inputs["new_title"]
    user_id = inputs["new_user_identifier"]
    
    payload = {
        "title": title,
        "userId": user_id
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    if response.status_code == 201:
        return None
    
    return response.json()