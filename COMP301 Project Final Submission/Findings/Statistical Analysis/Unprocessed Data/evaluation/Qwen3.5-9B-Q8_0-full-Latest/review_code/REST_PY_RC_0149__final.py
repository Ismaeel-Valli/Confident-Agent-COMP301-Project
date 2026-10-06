import requests

def solve(inputs):
    """
    Look up countries by exact match on their capital city using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The capital city name to match exactly
            - result_limit: Maximum number of results to return
            - included_attributes: List of country attributes to include in response
            - credential: Caller-supplied credential for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty
        Raises: Exception on unsuccessful HTTP response
    """
    # Build the API URL with query parameters
    base_url = "https://api.restcountries.com"
    
    # Construct the request URL with capital city as parameter
    url = f"{base_url}/v5/capital/{inputs['value']}"
    
    # Set up headers with the provided credential
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    # Make the GET request
    response = requests.get(url, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses
    if not response.ok:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for successful empty response, otherwise return the data
    if data is None or (isinstance(data, dict) and len(data) == 0):
        return None
    
    # Filter the results to include only the requested attributes
    if isinstance(data, list):
        filtered_results = []
        for country in data:
            if isinstance(country, dict):
                filtered_country = {key: value for key, value in country.items() 
                                  if key in inputs['included_attributes']}
                filtered_results.append(filtered_country)
        return filtered_results
    
    # If it's a single object (dict), filter it
    elif isinstance(data, dict):
        return {key: value for key, value in data.items() 
                if key in inputs['included_attributes']}
    
    # Return as-is if it's not a list or dict
    else:
        return data