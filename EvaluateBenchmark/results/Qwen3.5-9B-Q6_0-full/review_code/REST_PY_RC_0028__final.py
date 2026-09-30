def solve(inputs):
    """
    Look up countries by exact match on their two-letter ISO country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The two-letter ISO country code to match exactly
            - result_limit: Maximum number of results to return
            - included_attributes: List of attributes to include in the response
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        list or None: Decoded JSON response (list of countries) or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Extract inputs
    iso_code = inputs["value"]
    result_limit = inputs["result_limit"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build the API URL for exact match lookup by ISO code
    base_url = "https://api.restcountries.com/v5.0/country"
    url = f"{base_url}/{iso_code}"
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    # Make the GET request
    response = requests.get(url, headers=headers)
    
    # Check for unsuccessful HTTP response
    if response.status_code != 200:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
    
    # Decode JSON response
    data = response.json()
    
    # If no countries found (empty list), return None as per spec
    if not data:
        return None
    
    # Filter to only include requested attributes
    if included_attributes:
        filtered_data = []
        for country in data:
            filtered_country = {}
            for attr in included_attributes:
                if attr in country:
                    filtered_country[attr] = country[attr]
            filtered_data.append(filtered_country)
        return filtered_data
    
    # Return the full list (no filtering needed)
    return data