import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - included_fields (str): Comma-separated list of fields to return.
    
    Returns:
        dict or None: Decoded JSON response, or None for empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/users"
    
    # Parse included_fields
    fields_str = inputs.get("included_fields", "")
    if fields_str:
        fields = [f.strip() for f in fields_str.split(",")]
        query_params = {"fields": ",".join(fields)}
    else:
        query_params = {}
    
    response = requests.get(base_url, params=query_params)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    return response.json()