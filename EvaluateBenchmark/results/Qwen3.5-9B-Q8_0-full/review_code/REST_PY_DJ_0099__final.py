import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON with pagination support.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - included_fields (str): Comma-separated list of fields to include.
    
    Returns:
        dict or None: Decoded JSON response, or None for an empty successful response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/posts"
    
    # Parse included_fields
    fields_list = [f.strip() for f in inputs["included_fields"].split(",")]
    
    # Build query parameters - use 'limit' and 'skip' for pagination, 
    # and 'fields' to select specific fields
    params = {
        "limit": inputs["result_limit"],
        "skip": 0,
        "fields": ",".join(fields_list)
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        # DummyJSON returns a dict with 'posts' key and 'total' count
        # If no posts are returned, return None as per requirement
        if not data.get("posts") or len(data["posts"]) == 0:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")