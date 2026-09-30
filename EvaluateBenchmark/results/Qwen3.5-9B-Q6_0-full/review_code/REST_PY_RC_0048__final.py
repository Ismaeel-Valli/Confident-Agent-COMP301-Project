import requests

def solve(inputs):
    """
    Look up countries by exact match on their two-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The two-letter ISO country code to match exactly
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip
            - excluded_attributes: List of attributes to exclude from results
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    # Extract inputs
    iso_code = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    excluded_attributes = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Build the API URL for REST Countries v5 - use /country/{code} endpoint
    base_url = "https://api.restcountries.com/v5.0"
    url = f"{base_url}/country/{iso_code}"
    
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
        if excluded_attributes:
            filtered_data = []
            for country in data:
                filtered_country = {key: value for key, value in country.items() 
                                  if key not in excluded_attributes}
                filtered_data.append(filtered_country)
            return filtered_data
        
        return data
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")