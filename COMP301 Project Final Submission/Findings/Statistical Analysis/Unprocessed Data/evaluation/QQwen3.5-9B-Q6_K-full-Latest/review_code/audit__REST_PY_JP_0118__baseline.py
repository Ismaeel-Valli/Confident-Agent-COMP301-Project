import requests

def solve(inputs):
    """
    Submits a new album to JSONPlaceholder using the provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'new_title': The title for the new album.
            - 'new_user_identifier': The user ID for the new album.
    
    Returns:
        str or None: The title of the created album if present in the response, 
                     otherwise None for a successful empty response.
    
    Raises:
        requests.RequestException: If the HTTP request is unsuccessful.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/albums"
    
    payload = {
        "title": inputs['new_title'],
        "userId": inputs['new_user_identifier']
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise requests.RequestException(f"Failed to create album. Status code: {response.status_code}")
    
    data = response.json()
    
    if 'title' in data and data['title']:
        return data['title']
    else:
        return None