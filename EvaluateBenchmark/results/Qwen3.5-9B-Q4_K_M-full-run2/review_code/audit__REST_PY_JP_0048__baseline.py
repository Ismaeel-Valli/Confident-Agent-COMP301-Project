import requests

def solve(inputs):
    """
    Submits a new album to JSONPlaceholder using the provided inputs.
    
    Args:
        inputs (dict): A dictionary containing 'new_title' for the album title.
        
    Returns:
        int or None: The ID of the created album, or None if the response is empty.
        
    Raises:
        Exception: If the HTTP response indicates an error (non-2xx status code).
    """
    url = "https://jsonplaceholder.typicode.com/albums"
    
    payload = {
        "title": inputs.get("new_title")
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Failed to create album. HTTP Status Code: {response.status_code}, Response: {response.text}")
    
    # Check if the response is empty (e.g., status code 204 No Content)
    if not response.text.strip():
        return None
    
    data = response.json()
    
    # Return the id attribute if present, otherwise None
    return data.get("id")