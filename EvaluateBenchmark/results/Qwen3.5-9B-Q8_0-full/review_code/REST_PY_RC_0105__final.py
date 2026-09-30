import requests

def solve(inputs):
    """
    Look up countries by exact match on their subregion using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The subregion to match exactly
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip
            - included_attributes: List of attributes to include in the response
            - credential: Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response (list of countries) or None for empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build the query parameters
    params = {
        "subregion": inputs["value"],
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"],
        "fields": ",".join(inputs["included_attributes"])
    }
    
    # Make the API request with the provided credential
    response = requests.get(
        f"{base_url}/v5/countries",
        params=params,
        headers={"Authorization": f"Bearer {inputs['credential']}"}
    )
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for a successful empty response
    if not data:
        return None
    
    return data