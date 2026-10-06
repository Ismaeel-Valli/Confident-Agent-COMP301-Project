import requests

def solve(inputs):
    """
    Retrieve one page of todos from DummyJSON with pagination and field filtering.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return
            - included_fields (str): Comma-separated list of fields to include
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://dummyjson.com/todos"
    
    # Parse included_fields
    if inputs.get("included_fields"):
        fields_list = [f.strip() for f in inputs["included_fields"].split(",")]
    else:
        fields_list = None
    
    params = {
        "limit": inputs.get("result_limit", 10),
        "skip": 0,
        "select": ",".join(fields_list) if fields_list else None
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return the todos array or None if empty
    return data.get("todos") if data.get("todos") else None