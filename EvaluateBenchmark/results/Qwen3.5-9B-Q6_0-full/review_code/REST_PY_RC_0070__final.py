def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Three-letter ISO country code to match exactly
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip
            - excluded_attributes: List of attributes to exclude from results
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Extract inputs
    iso_code = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    excluded_attributes = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Build the API URL for REST Countries v5
    # Using /v3.1/countries/{code} endpoint for exact match by ISO code
    base_url = "https://api.restcountries.com/v3.1"
    url = f"{base_url}/countries/{iso_code}"
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Check for successful HTTP response
        if response.status_code != 200:
            raise Exception(f"HTTP error: status code {response.status_code}, message: {response.text}")
        
        # Decode JSON response
        data = response.json()
        
        # Handle empty response
        if not data:
            return None
        
        # Filter out excluded attributes from each country object
        filtered_results = []
        for country in data:
            filtered_country = {}
            for key, value in country.items():
                if key not in excluded_attributes:
                    filtered_country[key] = value
            filtered_results.append(filtered_country)
        
        # Apply pagination (skip and limit)
        paginated_results = filtered_results[results_to_skip:result_limit + results_to_skip]
        
        return paginated_results
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")