def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API,
    excluding specified attributes.
    
    Args:
        inputs (dict): Contains:
            - excluded_attributes (list): Attributes to exclude from response
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Base URL for REST Countries v5 API
    base_url = "https://api.restcountries.com/v5"
    
    # Prepare the request with credential in header
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    try:
        response = requests.get(base_url, headers=headers)
        
        # Check for successful HTTP status
        if response.status_code != 200:
            raise Exception(f"HTTP error: {response.status_code} - {response.text}")
        
        # Decode JSON response
        data = response.json()
        
        # If response is empty (empty list or None), return None
        if not data:
            return None
        
        # Filter out excluded attributes from each country object
        excluded = set(inputs.get('excluded_attributes', []))
        filtered_countries = []
        
        for country in data:
            filtered_country = {k: v for k, v in country.items() 
                              if k not in excluded}
            filtered_countries.append(filtered_country)
        
        return filtered_countries
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")