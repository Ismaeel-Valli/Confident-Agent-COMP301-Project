import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON with pagination support.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return
            - included_fields (str): Comma-separated list of fields to include
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://dummyjson.com/posts"
    
    # Build query parameters using standard parameter names
    params = {}
    
    # Add limit parameter (standard pagination)
    if inputs.get("result_limit") is not None:
        params["limit"] = inputs["result_limit"]
    
    # Add fields parameter for field selection
    if inputs.get("included_fields"):
        fields = [f.strip() for f in inputs["included_fields"].split(",")]
        params["fields"] = ",".join(fields)
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Check if posts array is empty
        if not data.get("posts"):
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")