import requests

def solve(inputs):
    """
    Retrieve one page of todos from DummyJSON with pagination.
    
    Args:
        inputs (dict): Must contain:
            - result_limit (int): Maximum number of results to return.
            - included_fields (str): Comma-separated list of fields to include.
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com"
    result_limit = inputs.get("result_limit")
    included_fields = inputs.get("included_fields", "")
    
    # Build query parameters
    params = {
        "limit": result_limit,
        "select": included_fields.split(",") if included_fields else None
    }
    
    response = requests.get(f"{base_url}/todos", params=params)
    response.raise_for_status()
    
    data = response.json()
    
    # Return the todos array or None if empty
    return data.get("todos") if data.get("todos") is not None else None