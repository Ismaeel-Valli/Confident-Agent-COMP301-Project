import requests

def solve(inputs):
    """
    Retrieves one page of users from DummyJSON based on included_fields.
    
    Args:
        inputs (dict): A dictionary containing 'included_fields' as a comma-separated string.
        
    Returns:
        dict or None: The decoded JSON response, or None if the response is empty but successful.
        
    Raises:
        requests.RequestException: If the HTTP response is unsuccessful.
    """
    # Extract included fields from inputs
    included_fields = inputs.get('included_fields', '')
    
    # Construct the API URL with query parameters for specific fields
    base_url = "https://jsonplaceholder.typicode.com/users"
    params = {}
    
    if included_fields:
        # Split the comma-separated string into a list and pass as 'fields' parameter
        # Note: DummyJSON (or similar APIs) might expect this format. 
        # Since standard JSONPlaceholder doesn't support field filtering via query params,
        # we assume the user's requirement implies an API that does, or we just fetch all.
        # However, to strictly follow "Retrieve one page of users" with "included_fields",
        # we will construct a URL that *would* work for an API supporting it.
        # For DummyJSON specifically (https://dummyjson.com/users), field filtering is done via query params like ?include=...
        # But standard practice for this specific prompt context usually implies JSONPlaceholder or similar.
        # Let's assume the user wants us to pass these fields as a query parameter named 'fields' or similar, 
        # OR simply fetch all if the API doesn't support it natively in that way.
        # Given the ambiguity and "DummyJSON" name (which often refers to https://dummyjson.com), 
        # let's try the dummyjson.com endpoint which supports ?include=field1,field2
        
        params['include'] = included_fields
    
    url = base_url if not params else f"{base_url}?{params.get('include', '')}"
    
    # Actually, let's stick to a more generic approach that works for both common APIs if the prompt implies standard behavior.
    # But the prompt says "DummyJSON". The popular one is https://dummyjson.com/users.
    # It supports ?include=field1,field2
    
    final_url = f"https://dummyjson.com/users?include={included_fields}" if included_fields else "https://dummyjson.com/users"
    
    try:
        response = requests.get(final_url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        # Check if the response is empty (e.g., users array is empty)
        if isinstance(data, dict) and 'users' in data:
            if not data['users']:
                return None
        
        return data

    except requests.RequestException as e:
        raise e