import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON with pagination and field filtering.
    
    Args:
        inputs (dict): Dictionary containing:
            - results_to_skip (int): Number of results to skip (offset)
            - included_fields (str): Comma-separated list of fields to include
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/users"
    
    # Parse included_fields
    if not inputs.get("included_fields"):
        fields_query = ""
    else:
        fields_query = ",".join(inputs["included_fields"].split(","))
    
    params = {
        "skip": inputs["results_to_skip"],
        "limit": 1,  # Retrieve one page (one result)
        "_fields": fields_query if fields_query else None
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data.get("users"):
        return None
    
    return data