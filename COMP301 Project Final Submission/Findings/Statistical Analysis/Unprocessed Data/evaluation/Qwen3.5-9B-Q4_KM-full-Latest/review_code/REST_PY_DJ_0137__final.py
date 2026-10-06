import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - included_fields (str): Comma-separated list of fields to return.
            - sort_field (str): Field used for ordering.
    
    Returns:
        dict or None: Decoded JSON response, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://dummyjson.com/posts"
    
    # Parse included_fields from comma-separated string into a list
    fields_list = [f.strip() for f in inputs["included_fields"].split(",")]
    
    # Build query parameters
    params = {
        "include_fields": ",".join(fields_list),
        "sort_by": inputs["sort_field"]
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    # Return None for successful empty response (posts array is empty)
    if not data.get("posts"):
        return None
    
    return data