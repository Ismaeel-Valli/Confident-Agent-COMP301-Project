import requests

def solve(inputs):
    """
    Retrieve one page of todos from DummyJSON, skipping specified results and selecting included fields.
    
    Args:
        inputs (dict): Dictionary containing:
            - results_to_skip (int): Number of results to skip.
            - included_fields (str): Comma-separated list of fields to return.
    
    Returns:
        dict or None: Decoded JSON response, or None for a successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/todos"
    
    # Parse included_fields
    if not inputs.get("included_fields"):
        included_fields = []
    else:
        included_fields = [field.strip() for field in inputs["included_fields"].split(",")]
    
    # Build query parameters
    params = {
        "skip": inputs.get("results_to_skip", 0),
        "limit": 1,  # Retrieve one page
    }
    
    # Add _fields only if there are included fields
    if included_fields:
        params["_fields"] = ",".join(included_fields)
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise exception for unsuccessful HTTP responses
        
        data = response.json()
        
        # Return the decoded JSON response
        return data
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")