import requests

def solve(inputs):
    """
    Submits a new album to JSONPlaceholder using the provided inputs dictionary.
    
    Args:
        inputs (dict): A dictionary containing 'new_title' for the album title.
        
    Returns:
        int or None: The ID of the created album, or None if the response is empty.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    url = "https://jsonplaceholder.typicode.com/albums"
    
    # Prepare the payload with the new title
    payload = {
        "title": inputs.get("new_title")
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create album. Status code: {response.status_code}, Response: {response.text}")
    
    # Check if the response is empty (no id in JSON body)
    data = response.json()
    if not data or "id" not in data:
        return None
        
    return data["id"]