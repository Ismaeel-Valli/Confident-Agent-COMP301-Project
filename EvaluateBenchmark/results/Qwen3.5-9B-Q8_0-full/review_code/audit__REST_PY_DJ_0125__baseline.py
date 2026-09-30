import requests

def solve(inputs):
    """
    Retrieves one page of users from DummyJSON based on skip count and sort field.
    
    Args:
        inputs (dict): Dictionary containing 'results_to_skip' and 'sort_field'.
        
    Returns:
        list or None: Decoded JSON response as a list, or None if the list is empty.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    base_url = "https://jsonplaceholder.typicode.com/users"
    
    # Extract parameters from inputs
    results_to_skip = inputs.get('results_to_skip', 0)
    sort_field = inputs.get('sort_field', 'id')
    
    # Construct the URL with query parameters
    params = {
        '_skip': results_to_skip,
        '_limit': 10,  # Retrieve one page (assuming 10 items per page as a standard)
        '_sort': sort_field
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for unsuccessful HTTP responses
        
        data = response.json()
        
        # Return None for a successful empty response
        if not data:
            return None
            
        return data
        
    except requests.RequestException as e:
        raise e