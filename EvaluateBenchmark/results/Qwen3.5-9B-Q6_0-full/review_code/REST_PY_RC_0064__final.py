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
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    # Extract inputs
    iso_code = inputs["value"]
    result_limit = inputs["result_limit"]
    excluded_attributes = inputs.get("excluded_attributes", [])
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
        
        # If the response is a list (multiple results), apply result_limit and filter excluded attributes
        if isinstance(data, list):
            # Apply result limit
            limited_data = data[:result_limit]
            
            # Filter out countries with excluded attributes
            filtered_data = []
            for country in limited_data:
                include_country = True
                for attr in excluded_attributes:
                    if attr in country:
                        include_country = False
                        break
                if include_country:
                    filtered_data.append(country)
            
            return filtered_data
        
        # If the response is a single object, apply result_limit (should be 1) and filter excluded attributes
        elif isinstance(data, dict):
            # Apply result limit (effectively 1 for single object)
            limited_data = [data]
            
            # Filter out countries with excluded attributes
            filtered_data = []
            for country in limited_data:
                include_country = True
                for attr in excluded_attributes:
                    if attr in country:
                        include_country = False
                        break
                if include_country:
                    filtered_data.append(country)
            
            return filtered_data
        
        # If the response is empty or None, return None as per specification
        elif data is None or (isinstance(data, list) and len(data) == 0):
            return None
        
        else:
            # Unexpected response format
            raise Exception(f"Unexpected response format: {type(data)}")
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")