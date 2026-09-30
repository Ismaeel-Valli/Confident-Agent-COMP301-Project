import requests

def solve(inputs):
    """
    Look up countries by exact currency code match from REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - value: Currency code to match exactly
            - result_limit: Maximum number of results
            - results_to_skip: Number of results to skip
            - included_attributes: List of attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response, or None for successful empty response
    """
    currency_code = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build the API URL with query parameters
    base_url = "https://api.restcountries.com/v5.0/countries"
    params = {
        "currency": currency_code,
        "limit": result_limit,
        "skip": results_to_skip,
        "fields": ",".join(included_attributes) if included_attributes else None
    }
    
    # Remove None from params to avoid URL encoding issues
    params = {k: v for k, v in params.items() if v is not None}
    
    # Make the request with credential (assumed to be a header or auth mechanism)
    headers = {"Authorization": f"Bearer {credential}"}
    
    response = requests.get(base_url, params=params, headers=headers)
    
    # Raise exception for unsuccessful HTTP response
    response.raise_for_status()
    
    # Decode JSON response
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data