import requests

def solve(inputs):
    """
    Update a photo in JSONPlaceholder with a new title.
    
    Args:
        inputs (dict): Must contain 'resource_id' and 'new_title'.
        
    Returns:
        str or None: The updated title from the response, or None if absent.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    resource_id = inputs['resource_id']
    new_title = inputs['new_title']
    
    url = f"https://jsonplaceholder.typicode.com/photos/{resource_id}"
    
    payload = {
        "title": new_title
    }
    
    response = requests.put(url, json=payload)
    response.raise_for_status()
    
    data = response.json()
    
    return data.get("title")