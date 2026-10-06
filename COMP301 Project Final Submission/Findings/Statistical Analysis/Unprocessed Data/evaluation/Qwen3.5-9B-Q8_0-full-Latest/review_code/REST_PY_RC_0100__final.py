import requests

def solve(inputs):
    """
    Look up countries by exact match on their subregion using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The subregion to match exactly
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip (for pagination)
            - credential: Caller-supplied authentication credential
    
    Returns:
        list or None: Decoded JSON response as a list, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    subregion = inputs["value"]
    limit = inputs["result_limit"]
    skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    # Build the query parameters
    params = {
        "subregion": subregion,
        "limit": limit,
        "skip": skip
    }
    
    # Make the API request with the provided credential
    response = requests.get(
        base_url + "/v5.0/countries",
        params=params,
        headers={"Authorization": f"Bearer {credential}"}
    )
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for successful empty response, otherwise return the data
    if len(data) == 0:
        return None
    
    return data