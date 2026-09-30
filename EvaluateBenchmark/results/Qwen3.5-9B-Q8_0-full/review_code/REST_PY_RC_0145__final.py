import requests

def solve(inputs):
    """
    Look up countries by exact match on their capital city using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The capital city to match exactly
            - results_to_skip: Number of results to skip
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    value = inputs["value"]
    results_to_skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    # Build the query parameters
    params = {
        "capital": value,
        "skip": results_to_skip
    }
    
    # Make the GET request with credentials in headers
    response = requests.get(
        base_url + "/v5/countries",
        params=params,
        headers={"Authorization": f"Bearer {credential}"}
    )
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data