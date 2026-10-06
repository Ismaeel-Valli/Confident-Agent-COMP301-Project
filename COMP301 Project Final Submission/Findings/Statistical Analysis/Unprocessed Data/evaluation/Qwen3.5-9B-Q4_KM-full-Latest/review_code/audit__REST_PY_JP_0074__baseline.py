import requests

def solve(inputs):
    """
    Submits a new album to JSONPlaceholder using the provided inputs dictionary.
    
    Args:
        inputs (dict): A dictionary containing at least 'new_title' for the album title.
        
    Returns:
        str or None: The title of the created album if present in the response, 
                     None if the response is empty but successful.
                     
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not in 2xx range).
    """
    url = "https://jsonplaceholder.typicode.com/albums"
    
    # Prepare the payload for the POST request
    payload = {
        "title": inputs.get("new_title")
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses (non-2xx status codes)
    if not response.ok:
        raise Exception(f"HTTP request failed with status code {response.status_code}: {response.text}")
    
    # Check if the response is empty
    if not response.json():
        return None
    
    # Return the title from the response
    data = response.json()
    return data.get("title")