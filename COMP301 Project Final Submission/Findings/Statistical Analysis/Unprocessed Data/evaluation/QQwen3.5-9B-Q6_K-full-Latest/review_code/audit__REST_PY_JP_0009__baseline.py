import requests

def solve(inputs):
    """
    Retrieves a comment by its identifier from JSONPlaceholder.
    
    Args:
        inputs (dict): A dictionary containing 'resource_id' (int).
        
    Returns:
        dict or None: The decoded JSON response if successful and data exists, 
                      None if the resource is not found (404).
                      
    Raises:
        requests.exceptions.RequestException: If an unsuccessful HTTP response occurs.
    """
    resource_id = inputs['resource_id']
    url = f"https://jsonplaceholder.typicode.com/comments/{resource_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        
        if response.status_code == 200:
            data = response.json()
            return data if data else None
        elif response.status_code == 404:
            return None
        else:
            raise requests.exceptions.HTTPError(f"HTTP error occurred: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        raise e