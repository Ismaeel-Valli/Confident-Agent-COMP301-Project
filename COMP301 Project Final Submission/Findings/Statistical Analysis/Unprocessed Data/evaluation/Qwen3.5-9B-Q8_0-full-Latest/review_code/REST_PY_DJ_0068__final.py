import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - included_fields (str): Comma-separated list of fields to include
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://dummyjson.com/posts"
    
    # Parse included_fields from comma-separated string
    if not inputs.get("included_fields"):
        params = {}
    else:
        params = {"includeFields": inputs["included_fields"]}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx/5xx)
        
        data = response.json()
        
        # DummyJSON returns a dict with 'posts' key containing the list
        # Return None if posts list is empty
        if not data.get("posts"):
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")