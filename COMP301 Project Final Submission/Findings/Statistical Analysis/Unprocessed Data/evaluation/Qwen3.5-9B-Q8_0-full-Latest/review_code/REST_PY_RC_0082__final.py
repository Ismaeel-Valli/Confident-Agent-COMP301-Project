import requests

def solve(inputs):
    """
    Look up countries by exact match on their common country name using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The exact country name to match
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip
            - excluded_attributes: List of attributes to exclude from results
            - credential: Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response (list of countries) or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build query parameters
    params = {
        'name': inputs['value'],
        'limit': inputs['result_limit'],
        'skip': inputs['results_to_skip']
    }
    
    # Make the request with the provided credential
    response = requests.get(
        f"{base_url}/v5/countries",
        params=params,
        headers={'Authorization': f'Bearer {inputs["credential"]}'}
    )
    
    # Raise exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode JSON response
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    # Exclude specified attributes from each country object
    if inputs['excluded_attributes']:
        for country in data:
            for attr in inputs['excluded_attributes']:
                if attr in country:
                    del country[attr]
    
    return data