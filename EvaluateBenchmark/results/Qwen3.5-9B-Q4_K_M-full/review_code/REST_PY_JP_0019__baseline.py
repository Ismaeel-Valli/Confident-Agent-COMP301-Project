import requests


def solve(inputs):
    """
    Retrieves photos from JSONPlaceholder using the provided inputs.
    
    Args:
        inputs (dict): A dictionary containing 'userId' and optionally 'page'.
        
    Returns:
        list or None: The decoded JSON response as a list of photo objects, 
                      or None if the response is empty.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    base_url = "https://jsonplaceholder.typicode.com/photos"
    
    # Extract parameters from inputs with defaults
    user_id = inputs.get("userId")
    page = inputs.get("page", 1)
    
    params = {
        "userId": user_id,
        "page": page
    }
    
    response = requests.get(base_url, params=params)
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    data = response.json()
    
    # Return None for a successful empty response
    if not data:
        return None
        
    return data