import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON with specified fields and sorting.
    
    Args:
        inputs (dict): Dictionary containing:
            - included_fields (str): Comma-separated list of fields to include
            - sort_field (str): Field to sort by
    
    Returns:
        dict or None: Decoded JSON response, or None if empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://dummyjson.com/users"
    
    # Build query parameters
    params = {}
    
    # Parse included fields - use comma-separated string as-is for API
    included_fields = inputs.get("included_fields", "")
    if included_fields:
        params["fields"] = included_fields
    
    # Add sort field if provided
    sort_field = inputs.get("sort_field", "")
    if sort_field:
        params["sort"] = sort_field
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for empty users array
    if not data.get("users"):
        return None
    
    return data