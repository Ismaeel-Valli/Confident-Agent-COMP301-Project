import requests

def solve(inputs):
    """
    Look up countries by exact match on their two-letter ISO country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Two-letter ISO country code to match exactly
            - result_limit (int): Maximum number of results to return
            - results_to_skip (int): Number of results to skip
            - included_attributes (list): List of attributes to include in the response
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build query parameters
    params = {
        "value": inputs["value"],
        "result_limit": inputs["result_limit"],
        "results_to_skip": inputs["results_to_skip"],
        "included_attributes": ",".join(inputs["included_attributes"])
    }
    
    # Make the API request with the provided credential
    response = requests.get(
        f"{base_url}/v5/country",
        params=params,
        headers={"Authorization": inputs["credential"]}
    )
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode and return the JSON response
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data