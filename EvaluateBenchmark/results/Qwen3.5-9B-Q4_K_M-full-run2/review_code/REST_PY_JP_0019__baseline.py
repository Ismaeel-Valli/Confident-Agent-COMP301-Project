import requests

def solve(inputs):
    """
    Retrieves photos from JSONPlaceholder using the provided inputs (assumed to be a list of IDs).
    
    Args:
        inputs (list): A list of photo IDs to retrieve.
        
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
        
    Raises:
        requests.RequestException: If the HTTP response is unsuccessful.
    """
    base_url = "https://jsonplaceholder.typicode.com/photos"
    
    # Prepare the request payload with the provided inputs (IDs)
    params = {"ids": inputs}
    
    try:
        response = requests.get(base_url, params=params)
        
        # Raise an exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Decode the JSON response
        data = response.json()
        
        # Return None for a successful empty response
        if not data:
            return None
            
        return data
        
    except requests.RequestException as e:
        raise e