def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Contains:
            - "value": The three-letter ISO country code to match exactly
            - "excluded_attributes": List of attributes to exclude from results
            - "credential": Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response. None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    import requests
    
    # Extract inputs
    iso_code = inputs["value"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    credential = inputs["credential"]
    
    # Build API URL for REST Countries v5
    # Using the /v3.1/countries endpoint with alpha-3 code filter
    base_url = "https://api.restcountries.com/v3.1"
    url = f"{base_url}/countries/{iso_code}"
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Check for unsuccessful HTTP response
        if not response.ok:
            raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
        
        # Decode JSON response
        data = response.json()
        
        # Filter out excluded attributes if any
        if excluded_attributes:
            filtered_data = {}
            for key, value in data.items():
                if key not in excluded_attributes:
                    filtered_data[key] = value
            return filtered_data
        
        return data
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")