import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON, skipping specified results
    and including only specified fields.
    
    Args:
        inputs (dict): Dictionary containing:
            - results_to_skip (int): Number of results to skip
            - included_fields (str): Comma-separated list of fields to include
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://dummyjson.com/posts"
    
    # Parse included_fields
    if not inputs.get("included_fields"):
        fields_query = ""
    else:
        fields_query = ",".join(inputs["included_fields"].split(","))
    
    # Build query parameters
    params = {
        "skip": inputs.get("results_to_skip", 0),
        "limit": 1,  # Retrieve one page
        "_fields": fields_query if fields_query else None
    }
    
    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Return the posts array or None if empty
        return data.get("posts")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")