import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - results_to_skip (int): Number of results to skip.
            - included_fields (str): Comma-separated list of fields to return.
    
    Returns:
        dict or None: Decoded JSON response, or None for a successful empty response.
    
    Raises:
        Exception: For an unsuccessful HTTP response.
    """
    base_url = "https://dummyjson.com"
    endpoint = "/posts"
    
    # Build query parameters
    params = {
        "skip": inputs["results_to_skip"],
        "limit": 1,  # Retrieve one page (one result)
    }
    
    # Parse included_fields into a list
    fields_list = [f.strip() for f in inputs["included_fields"].split(",")]
    
    # Build the query string with only the requested fields
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    if fields_list:
        query_string += f"&fields={','.join(fields_list)}"
    
    url = base_url + endpoint + "?" + query_string
    
    try:
        response = requests.get(url)
        
        # Raise an exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Decode the JSON response
        data = response.json()
        
        return data
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Unsuccessful HTTP response: {e}")