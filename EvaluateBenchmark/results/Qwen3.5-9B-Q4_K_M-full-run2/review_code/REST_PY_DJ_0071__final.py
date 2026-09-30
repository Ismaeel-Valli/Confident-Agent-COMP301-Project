import requests

def solve(inputs):
    """
    Retrieve one page of todos from DummyJSON using the included_fields filter.
    
    Args:
        inputs (dict): Dictionary containing:
            - 'included_fields' (str): Comma-separated list of fields to return.
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
    
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    base_url = "https://dummyjson.com"
    endpoint = "/todos"
    
    included_fields = inputs.get("included_fields", "")
    
    params = {}
    if included_fields:
        params["fields"] = included_fields
    
    url = f"{base_url}{endpoint}"
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    return response.json()