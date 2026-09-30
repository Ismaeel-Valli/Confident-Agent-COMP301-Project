import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON with specified fields and sorting.
    
    Args:
        inputs (dict): Dictionary containing:
            - included_fields (str): Comma-separated list of fields to include
            - sort_field (str): Field to sort by
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://dummyjson.com/users"
    
    # Parse included_fields from comma-separated string
    fields_list = inputs["included_fields"].split(",") if inputs["included_fields"] else []
    
    # Build query parameters - use include instead of include_fields
    params = {}
    if fields_list:
        params["include"] = ",".join(fields_list)
    params["sort_by"] = inputs["sort_field"]
    
    # Make the GET request
    response = requests.get(base_url, params=params)
    
    # Raise exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode JSON response
    data = response.json()
    
    # Return None for empty successful response (empty users array)
    if not data.get("users"):
        return None
    
    return data