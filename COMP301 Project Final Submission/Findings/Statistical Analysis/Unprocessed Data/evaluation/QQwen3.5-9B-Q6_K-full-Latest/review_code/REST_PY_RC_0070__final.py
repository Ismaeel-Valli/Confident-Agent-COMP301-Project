def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Three-letter ISO country code to match exactly
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip
            - excluded_attributes: List of attributes to exclude from results
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Extract inputs with validation
    value = inputs.get("value")
    result_limit = inputs.get("result_limit")
    results_to_skip = inputs.get("results_to_skip", 0)
    excluded_attributes = inputs.get("excluded_attributes", [])
    credential = inputs.get("credential")
    
    # Validate required fields
    if value is None:
        raise ValueError("Missing required field: 'value'")
    
    # Build the API URL for REST Countries v5
    # Using the /v3/countries/{code} endpoint for exact match lookup
    base_url = "https://api.restcountries.com/v3"
    url = f"{base_url}/countries/{value}"
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Check for unsuccessful HTTP response
        if not response.ok:
            raise Exception(f"HTTP error: {response.status_code} - {response.text}")
        
        # Decode JSON response
        data = response.json()
        
        # Handle empty response
        if data is None or (isinstance(data, list) and len(data) == 0):
            return None
        
        # Apply result_limit if specified
        if result_limit is not None:
            data = data[:result_limit]
        
        # Apply results_to_skip if specified
        if results_to_skip > 0:
            data = data[results_to_skip:]
        
        # Exclude specified attributes from each country object
        if excluded_attributes:
            filtered_data = []
            for country in data:
                filtered_country = {
                    key: value 
                    for key, value in country.items() 
                    if key not in excluded_attributes
                }
                filtered_data.append(filtered_country)
            data = filtered_data
        
        return data
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")