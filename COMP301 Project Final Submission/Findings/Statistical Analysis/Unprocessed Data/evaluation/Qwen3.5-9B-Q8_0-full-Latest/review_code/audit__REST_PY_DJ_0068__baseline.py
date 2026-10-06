import requests

def solve(inputs):
    """
    Retrieves one page of posts from DummyJSON based on included_fields.
    
    Args:
        inputs (dict): A dictionary containing 'included_fields' as a comma-separated string.
        
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    included_fields = inputs.get('included_fields', '')
    
    # Construct the URL with query parameters
    url = "https://jsonplaceholder.typicode.com/posts"
    params = {}
    
    if included_fields:
        params['fields'] = included_fields
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        # Return None if the response is empty (though DummyJSON posts endpoint rarely returns empty lists without filtering)
        if not data:
            return None
            
        return data
        
    except requests.exceptions.HTTPError as errh:
        raise Exception(f"HTTP Error occurred: {errh}")
    except requests.exceptions.RequestException as err:
        raise Exception(f"Request failed: {err}")