import requests


def solve(inputs):
    """
    Look up countries by exact match on their calling code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The calling code to match exactly
            - result_limit: Maximum number of results to return
            - excluded_attributes: List of country attributes to exclude from response
            - credential: Caller-supplied credential for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build the API endpoint URL with calling code parameter
    url = f"{base_url}/v5.0/calling-code/{inputs['value']}"
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    params = {
        "limit": inputs["result_limit"]
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        # Check for unsuccessful HTTP response
        if not response.ok:
            raise Exception(f"HTTP error: {response.status_code} - {response.text}")
        
        # Decode JSON response
        data = response.json()
        
        # Return None for successful empty response
        if data is None or (isinstance(data, list) and len(data) == 0):
            return None
        
        # Filter out excluded attributes from each country object
        if inputs["excluded_attributes"]:
            filtered_data = []
            for country in data:
                filtered_country = {k: v for k, v in country.items() 
                                  if k not in inputs["excluded_attributes"]}
                filtered_data.append(filtered_country)
            return filtered_data
        
        return data
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")