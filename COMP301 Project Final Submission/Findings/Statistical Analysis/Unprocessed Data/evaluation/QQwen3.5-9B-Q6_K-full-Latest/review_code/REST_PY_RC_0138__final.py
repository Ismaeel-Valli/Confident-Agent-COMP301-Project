import requests

def solve(inputs):
    """
    Look up countries by exact match on their calling code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The calling code to match exactly
            - result_limit: Maximum number of results to return
            - excluded_attributes: List of country attributes to exclude from response
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    # Build the API URL for REST Countries v5
    base_url = "https://api.restcountries.com"
    
    # Extract inputs
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    excluded_attributes = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Construct the API endpoint for calling code lookup
    url = f"{base_url}/v5.1/calling-code/{value}"
    
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
        
        # If empty response, return None as per specification
        if data is None or (isinstance(data, list) and len(data) == 0):
            return None
        
        # Filter out excluded attributes from each country object
        filtered_countries = []
        for country in data:
            filtered_country = {}
            for key, val in country.items():
                if key not in excluded_attributes:
                    filtered_country[key] = val
            filtered_countries.append(filtered_country)
        
        # Apply result limit
        return filtered_countries[:result_limit]
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")