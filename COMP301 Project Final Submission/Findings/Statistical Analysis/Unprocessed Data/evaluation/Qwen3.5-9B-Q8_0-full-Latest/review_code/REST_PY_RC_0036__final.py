import requests

def solve(inputs):
    """
    Look up countries by exact match on their two-letter ISO country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): The two-letter ISO country code to match exactly.
            - results_to_skip (int): Number of results to skip.
            - included_attributes (list): List of attributes to return.
            - credential (str): Caller-supplied credential with necessary permissions.
    
    Returns:
        dict or None: Decoded JSON response, or None for a successful empty response.
    
    Raises:
        Exception: For an unsuccessful HTTP response.
    """
    base_url = "https://api.restcountries.com"
    country_code = inputs["value"]
    skip = inputs["results_to_skip"]
    attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build the query parameters
    params = {
        "code": country_code,
        "skip": skip,
        "fields": ",".join(attributes) if attributes else None
    }
    
    # Remove None from params to avoid sending it in the request
    params = {k: v for k, v in params.items() if v is not None}
    
    # Make the API request with the provided credential
    headers = {"Authorization": f"Bearer {credential}"}
    response = requests.get(f"{base_url}/v5/country", params=params, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for a successful empty response
    if not data:
        return None
    
    return data