import requests

def solve(inputs):
    """
    Retrieves a comment by its identifier from JSONPlaceholder.
    
    Args:
        inputs (dict): A dictionary containing 'resource_id' (int) for the comment ID.
        
    Returns:
        dict or None: The decoded JSON response if successful and not empty, 
                      or None if the response is successfully empty.
                      
    Raises:
        Exception: If the HTTP response is unsuccessful (non-2xx status code).
    """
    resource_id = inputs.get('resource_id')
    
    url = f"https://jsonplaceholder.typicode.com/comments/{resource_id}"
    
    try:
        response = requests.get(url)
        
        # Raise an exception for unsuccessful HTTP responses (non-2xx status codes)
        response.raise_for_status()
        
        # Decode the JSON response
        data = response.json()
        
        # Return None for a successful empty response
        if not data:
            return None
            
        return data
        
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Unsuccessful HTTP response: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")