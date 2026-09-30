import requests

def solve(inputs):
    """
    Retrieves one page of posts from DummyJSON based on provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'included_fields' (str): Comma-separated list of fields to return.
            - 'sort_field' (str): Field used for ordering the results.
    
    Returns:
        dict or None: The decoded JSON response if successful and non-empty, 
                      None if the response is empty but successful.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    base_url = "https://jsonplaceholder.typicode.com/posts"
    
    # Parse included_fields
    included_fields = inputs.get('included_fields', '')
    if included_fields:
        fields_list = [field.strip() for field in included_fields.split(',')]
        params = {
            '_fields': ','.join(fields_list),
            'sort': inputs.get('sort_field', 'id')
        }
    else:
        params = {
            'sort': inputs.get('sort_field', 'id')
        }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        if not data:
            return None
        
        return data
    
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)