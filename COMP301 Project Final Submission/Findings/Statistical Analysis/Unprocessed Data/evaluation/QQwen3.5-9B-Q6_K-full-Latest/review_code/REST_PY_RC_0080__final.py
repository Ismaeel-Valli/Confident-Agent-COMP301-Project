def solve(inputs):
    """
    Look up countries by exact match on their common country name using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Country name to match exactly
            - results_to_skip (int): Number of results to skip
            - excluded_attributes (list): Attributes to exclude from response
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Build the API URL with query parameters
    base_url = "https://api.restcountries.com/v5"
    params = {
        "name": inputs["value"],
        "skip": inputs["results_to_skip"]
    }
    
    # Make the request with credential in headers
    response = requests.get(base_url, params=params, headers={"Authorization": f"Bearer {inputs['credential']}"})
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If empty response, return None as per spec
    if not data:
        return None
    
    # Filter out excluded attributes if any
    if inputs["excluded_attributes"]:
        filtered_data = []
        for country in data:
            filtered_country = {k: v for k, v in country.items() 
                              if k not in inputs["excluded_attributes"]}
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data