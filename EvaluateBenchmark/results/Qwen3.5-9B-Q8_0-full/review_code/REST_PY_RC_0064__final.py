import requests

def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Three-letter ISO country code to match exactly
            - result_limit: Maximum number of results to return
            - excluded_attributes: List of country attributes to exclude from response
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    # Extract inputs
    iso_code = inputs["value"]
    result_limit = inputs["result_limit"]
    excluded_attributes = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Build the API URL for REST Countries v5
    # Using the /v3.1/countries/{code} endpoint for exact match by ISO code
    base_url = "https://api.restcountries.com"
    url = f"{base_url}/v3.1/countries/{iso_code}"
    
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
        
        # Handle empty response
        if data is None or (isinstance(data, list) and len(data) == 0):
            return None
        
        # Filter out excluded attributes from each country object
        if isinstance(data, list):
            filtered_data = []
            for country in data:
                if isinstance(country, dict):
                    filtered_country = {k: v for k, v in country.items() 
                                      if k not in excluded_attributes}
                    filtered_data.append(filtered_country)
            return filtered_data
        
        # If it's a single object (dict), filter attributes
        elif isinstance(data, dict):
            filtered_data = {k: v for k, v in data.items() 
                           if k not in excluded_attributes}
            return filtered_data
        
        return data
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")