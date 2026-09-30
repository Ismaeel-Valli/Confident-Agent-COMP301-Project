import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - included_fields (str): Comma-separated list of fields to return
            - sort_field (str): Field used for ordering
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty response
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://dummyjson.com/posts"
    
    # Parse included_fields from comma-separated string
    fields = [f.strip() for f in inputs["included_fields"].split(",")]
    
    # Build query parameters
    params = {
        "include_fields": ",".join(fields),
        "sort_by": inputs["sort_field"]
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Return None for successful empty response (posts array is empty)
        if not data.get("posts"):
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")