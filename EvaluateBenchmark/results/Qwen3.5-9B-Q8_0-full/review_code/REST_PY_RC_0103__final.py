import requests

def solve(inputs):
    """
    Look up countries by exact match on their subregion using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The subregion to match exactly
            - results_to_skip: Number of results to skip (for pagination)
            - included_attributes: List of attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    """
    base_url = "https://api.restcountries.com"
    
    # Build the query parameters
    params = {
        "subregion": inputs["value"],
        "skip": inputs["results_to_skip"]
    }
    
    # Make the GET request
    response = requests.get(f"{base_url}/v5/countries", params=params)
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for successful empty response, otherwise return the data
    if not data:
        return None
    
    return data