import requests

def solve(inputs):
    """
    Retrieves one page of users from DummyJSON based on provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'included_fields' (str): Comma-separated list of fields to include.
            - 'sort_field' (str): Field name for sorting the results.
    
    Returns:
        list or None: The decoded JSON response as a list of users, or None if the response is empty.
    
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    base_url = "https://dummyjson.com/users"
    
    # Prepare query parameters
    params = {
        'include_fields': inputs['included_fields'],
        'sort': inputs['sort_field']
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        # DummyJSON returns a 'users' key in the response
        users = data.get('users', [])
        
        return users if users else None
        
    except requests.RequestException as e:
        raise e