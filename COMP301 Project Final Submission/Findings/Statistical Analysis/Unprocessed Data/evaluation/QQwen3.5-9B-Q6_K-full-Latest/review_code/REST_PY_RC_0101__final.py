import requests

def solve(inputs):
    """
    Look up countries by exact match on their subregion using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The subregion to match exactly
            - result_limit: Maximum number of results to return
            - included_attributes: List of attributes to include in the response
            - credential: Caller-supplied credential for authentication
    
    Returns:
        list or None: Decoded JSON response, or None if successful but empty
        Raises: Exception for unsuccessful HTTP responses
    """
    # Build the API URL with query parameters
    base_url = "https://api.restcountries.com/v5"
    
    # Prepare query parameters
    params = {
        'subregion': inputs['value'],
        'limit': inputs['result_limit']
    }
    
    # Make the GET request with credentials in headers
    response = requests.get(
        base_url,
        params=params,
        headers={'Authorization': f'Bearer {inputs["credential"]}'}
    )
    
    # Check for successful HTTP response
    if response.status_code != 200:
        raise Exception(f"HTTP error occurred: {response.status_code}")
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for successful empty response, otherwise return the data
    if not data:
        return None
    
    # Filter to only include requested attributes
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