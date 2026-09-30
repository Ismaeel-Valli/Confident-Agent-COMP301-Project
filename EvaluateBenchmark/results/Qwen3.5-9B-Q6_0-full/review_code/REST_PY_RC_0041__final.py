def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - results_to_skip (int): Number of results to skip
            - included_attributes (list): Attributes to include in response
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    base_url = "https://api.restcountries.com/v5.1/countries/all"
    
    # Build query parameters
    params = {
        "skip": inputs["results_to_skip"],
        "credential": inputs["credential"]
    }
    
    # Make the request
    response = requests.get(base_url, params=params)
    
    # Check for unsuccessful HTTP response
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    # Decode JSON response
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    # Filter to included attributes if specified
    if inputs["included_attributes"]:
        filtered_data = {}
        for key in inputs["included_attributes"]:
            if key in data:
                filtered_data[key] = data[key]
        return filtered_data
    
    return data