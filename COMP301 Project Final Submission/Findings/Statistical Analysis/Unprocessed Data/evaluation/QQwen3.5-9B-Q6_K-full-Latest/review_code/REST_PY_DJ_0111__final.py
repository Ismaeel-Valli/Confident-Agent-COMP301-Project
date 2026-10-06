import requests

def solve(inputs):
    """
    Retrieve one page of todos from DummyJSON with pagination and field filtering.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - results_to_skip (int): Number of results to skip.
            - included_fields (str): Comma-separated list of fields to include.
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/todos"
    
    # Parse included_fields
    if not inputs.get("included_fields"):
        included_fields = []
    else:
        included_fields = [f.strip() for f in inputs["included_fields"].split(",") if f.strip()]
    
    params = {
        "limit": inputs.get("result_limit", 10),
        "skip": inputs.get("results_to_skip", 0)
    }
    
    # Only add _fields if there are fields to include
    if included_fields:
        params["_fields"] = ",".join(included_fields)
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # DummyJSON returns a dict with 'todos' key and 'total' count
    # If no todos, return None as per requirement for empty successful response
    if not data.get("todos"):
        return None
    
    return data