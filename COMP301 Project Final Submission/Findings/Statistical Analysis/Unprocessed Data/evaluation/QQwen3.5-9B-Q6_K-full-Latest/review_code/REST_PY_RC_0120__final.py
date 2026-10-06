def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Currency code to match exactly
            - result_limit (int): Maximum number of results
            - credential (str): Caller-supplied API key
    
    Returns:
        list or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    import requests
    
    # Build the API URL with query parameters
    base_url = "https://api.restcountries.com/v5"
    params = {
        "currency": inputs["value"],
        "limit": inputs["result_limit"]
    }
    
    # Make the request with the provided credential
    headers = {"Authorization": f"Bearer {inputs['credential']}"}
    response = requests.get(base_url, params=params, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for empty successful response, otherwise return the data
    if len(data) == 0:
        return None
    
    return data