import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON with pagination support.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - included_fields (str): Comma-separated list of fields to include.
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/users"
    result_limit = inputs.get("result_limit")
    included_fields = inputs.get("included_fields", "")
    
    # Build query parameters
    params = {}
    if result_limit is not None:
        params["limit"] = result_limit
    
    if included_fields:
        fields_list = [f.strip() for f in included_fields.split(",")]
        params["fields"] = ",".join(fields_list)
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        # DummyJSON returns {"users": [...], "total": ..., "skip": ..., "limit": ...}
        # If users list is empty, return None as per requirement
        if not data.get("users"):
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")