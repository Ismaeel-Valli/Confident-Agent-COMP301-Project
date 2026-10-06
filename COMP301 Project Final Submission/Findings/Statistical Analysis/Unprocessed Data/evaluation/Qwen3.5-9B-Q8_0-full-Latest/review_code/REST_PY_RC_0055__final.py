import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return
            - results_to_skip (int): Number of results to skip
            - included_attributes (list): List of attributes to include in response
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build query parameters
    params = {
        'limit': inputs['result_limit'],
        'skip': inputs['results_to_skip']
    }
    
    # Make the request with the provided credential
    response = requests.get(
        f"{base_url}/v5/countries",
        params=params,
        headers={'Authorization': f'Bearer {inputs["credential"]}'}
    )
    
    # Check for unsuccessful HTTP response
    if not response.ok:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    # Decode JSON response
    data = response.json()
    
    # Filter to only included attributes if specified
    if inputs['included_attributes']:
        filtered_data = []
        for country in data:
            filtered_country = {}
            for attr in inputs['included_attributes']:
                if attr in country:
                    filtered_country[attr] = country[attr]
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data