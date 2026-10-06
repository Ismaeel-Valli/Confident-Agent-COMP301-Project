import requests

def solve(inputs):
    """
    Look up countries by exact match on their two-letter ISO country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The two-letter ISO country code to match exactly
            - result_limit: Maximum number of results to return
            - included_attributes: List of attributes to include in the response
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build the API endpoint for exact match lookup
    country_code = inputs["value"]
    limit = inputs["result_limit"]
    attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Construct query parameters
    params = {
        "code": country_code,
        "limit": limit,
        "fields": ",".join(attributes)
    }
    
    # Make the API request with the provided credential
    headers = {"Authorization": f"Bearer {credential}"}
    response = requests.get(f"{base_url}/v5/country", params=params, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode and return the JSON response
    data = response.json()
    
    # Return None for successful empty response (empty list)
    if not data:
        return None
    
    return data