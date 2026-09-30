import requests

def solve(inputs):
    """
    Retrieves one page of products from DummyJSON based on specified fields.
    
    Args:
        inputs (dict): A dictionary containing 'included_fields' as a comma-separated string.
        
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    included_fields = inputs.get('included_fields', '')
    
    # Construct the URL with query parameters for fields
    url = "https://jsonplaceholder.typicode.com/products"
    params = {'fields': included_fields} if included_fields else {}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for unsuccessful HTTP responses
        
        data = response.json()
        
        # Return None for a successful empty response
        if not data:
            return None
            
        return data
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"HTTP request failed: {e}")