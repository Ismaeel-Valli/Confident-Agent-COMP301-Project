import requests

def solve(inputs):
    """
    Retrieves a comment by its identifier from JSONPlaceholder.
    
    Args:
        inputs (dict): A dictionary containing 'resource_id' (int).
        
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
        
    Raises:
        requests.RequestException: If the HTTP response is unsuccessful.
    """
    resource_id = inputs['resource_id']
    url = f"https://jsonplaceholder.typicode.com/comments/{resource_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        if response.status_code == 200 and not response.text.strip():
            return None
            
        return response.json()
        
    except requests.RequestException as e:
        raise e