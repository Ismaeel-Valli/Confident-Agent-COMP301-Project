import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - included_fields (str): Comma-separated list of fields to return
            - sort_field (str): Field used for ordering
    
    Returns:
        dict or None: Decoded JSON response, or None if empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://dummyjson.com/posts"
    
    # Parse included_fields
    fields_list = inputs["included_fields"].split(",") if inputs["included_fields"] else []
    
    # Build query parameters
    params = {
        "limit": 1,  # Retrieve one page
        "include_fields": ",".join(fields_list) if fields_list else None,
        "sort_by": inputs["sort_field"]
    }
    
    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Return None for successful empty response
        if not data.get("posts") or len(data["posts"]) == 0:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")