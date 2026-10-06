import requests

def solve(inputs):
    """
    Retrieve one page of todos from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - 'included_fields': str, comma-separated list of fields to return
    
    Returns:
        dict or None: Decoded JSON response, or None for empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://dummyjson.com"
    endpoint = "/todos"
    
    # Parse included_fields from comma-separated string
    if 'included_fields' not in inputs:
        raise ValueError("Missing required key 'included_fields'")
    
    included_fields = inputs['included_fields']
    
    # Build query parameters for fields to include
    params = {}
    if included_fields:
        # Split by comma and strip whitespace
        field_list = [f.strip() for f in included_fields.split(',') if f.strip()]
        if field_list:
            params['fields'] = ','.join(field_list)
    
    url = base_url + endpoint
    
    try:
        response = requests.get(url, params=params)
        
        # Check for unsuccessful HTTP response
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        
        # Decode JSON response
        data = response.json()
        
        # Return None for empty response (todos array is empty)
        if not data.get('todos') or len(data['todos']) == 0:
            return None
        
        return data
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")