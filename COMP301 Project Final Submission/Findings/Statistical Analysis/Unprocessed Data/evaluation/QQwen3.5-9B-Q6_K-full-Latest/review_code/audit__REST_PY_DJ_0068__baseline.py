import requests

def solve(inputs):
    """
    Retrieves one page of posts from DummyJSON based on specified included fields.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'included_fields' (str): Comma-separated list of fields to include in the response.
    
    Returns:
        dict or None: The decoded JSON response if successful and non-empty, otherwise None.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request is unsuccessful.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    posts_endpoint = f"{base_url}/posts"
    
    # Parse included_fields from comma-separated string into a list
    included_fields = inputs.get('included_fields', '').split(',') if inputs.get('included_fields') else []
    
    # Prepare query parameters for the request
    params = {
        '_limit': 1,  # Retrieve one page (one post)
        '_include': ','.join(included_fields) if included_fields else None
    }
    
    try:
        response = requests.get(posts_endpoint, params=params)
        response.raise_for_status()  # Raise an exception for unsuccessful HTTP responses
        
        data = response.json()
        
        # Return None for a successful empty response
        if not data:
            return None
            
        return data
    
    except requests.exceptions.RequestException as e:
        raise e