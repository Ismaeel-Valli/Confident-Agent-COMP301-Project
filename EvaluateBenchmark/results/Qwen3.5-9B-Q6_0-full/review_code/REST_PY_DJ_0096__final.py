import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON with pagination support.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return
            - included_fields (str): Comma-separated list of fields to include
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://dummyjson.com/users"
    
    # Build query parameters
    params = {}
    
    # Set result limit
    if inputs.get("result_limit") is not None:
        params["limit"] = inputs["result_limit"]
    
    # Parse included_fields - use include_fields parameter for filtering
    if inputs.get("included_fields"):
        fields_list = [f.strip() for f in inputs["included_fields"].split(",")]
        params["include_fields"] = ",".join(fields_list)
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if the response is empty (no users)
            if not data.get("users") or len(data["users"]) == 0:
                return None
            
            return data
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")