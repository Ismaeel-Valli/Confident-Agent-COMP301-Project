def solve(inputs):
    """
    Retrieve one page of todos from DummyJSON with pagination and field filtering.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - results_to_skip (int): Number of results to skip.
            - included_fields (str): Comma-separated list of fields to include.
    
    Returns:
        dict or None: Decoded JSON response, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    import requests
    
    base_url = "https://dummyjson.com/todos"
    
    # Parse included_fields
    fields_list = [f.strip() for f in inputs["included_fields"].split(",")]
    
    params = {
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"],
        "fields": ",".join(fields_list)
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    data = response.json()
    
    # DummyJSON returns a dict with "todos" key; return the list of todos
    return data["todos"]