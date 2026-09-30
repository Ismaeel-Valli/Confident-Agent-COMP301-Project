import requests

def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The three-letter ISO country code to match exactly
            - results_to_skip: Number of results to skip
            - included_attributes: List of attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build the query URL with exact match on three-letter ISO code
    url = f"{base_url}/v5.0/country/{inputs['value']}"
    
    # Make the request with the provided credential
    response = requests.get(url, headers={"Authorization": inputs["credential"]})
    
    # Raise exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # If no results found, return None
    if not data:
        return None
    
    # Filter to only include requested attributes
    if inputs["included_attributes"]:
        filtered_data = {}
        for attr in inputs["included_attributes"]:
            if attr in data:
                filtered_data[attr] = data[attr]
        return filtered_data
    
    return data