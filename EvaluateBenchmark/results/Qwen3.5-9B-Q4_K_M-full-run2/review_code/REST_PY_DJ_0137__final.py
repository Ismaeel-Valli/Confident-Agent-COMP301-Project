import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - included_fields (str): Comma-separated list of fields to return.
            - sort_field (str): Field used for ordering.
    
    Returns:
        dict or None: Decoded JSON response, or None if empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com"
    endpoint = "/posts"
    
    params = {
        "skip": 0,
        "limit": 1,
        "sort_by": inputs["sort_field"],
        "include_fields": inputs["included_fields"]
    }
    
    response = requests.get(f"{base_url}{endpoint}", params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    if not data.get("posts"):
        return None
    
    return data