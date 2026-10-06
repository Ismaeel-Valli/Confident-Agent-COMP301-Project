import requests

def solve(inputs):
    """
    Retrieve one page of todos from DummyJSON with pagination and field filtering.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return
            - included_fields (str): Comma-separated list of fields to include
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://dummyjson.com/todos"
    
    # Parse included_fields
    included_fields = [f.strip() for f in inputs["included_fields"].split(",")]
    
    # Build query parameters - use 'fields' as per DummyJSON API
    params = {
        "limit": inputs["result_limit"],
        "fields": ",".join(included_fields)
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx/5xx)
        
        data = response.json()
        
        # Return None if successful but empty
        if not data.get("todos"):
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")