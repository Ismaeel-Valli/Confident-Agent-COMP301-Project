import requests

def solve(inputs):
    """
    Look up countries by exact match on two-letter ISO country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Two-letter ISO country code to match exactly
            - results_to_skip: Number of results to skip
            - included_attributes: List of attributes to include in response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    country_code = inputs["value"]
    skip = inputs["results_to_skip"]
    attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "code": country_code,
        "skip": skip,
        "fields": ",".join(attributes) if attributes else None
    }
    
    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}
    
    # Make the request with credential (assumed to be a header or auth mechanism)
    headers = {"Authorization": f"Bearer {credential}"}
    
    response = requests.get(f"{base_url}/v5.0/country", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # REST Countries v5 returns a list of countries or a single country object
    # For exact match, we expect either a list with one item or a single object
    if isinstance(data, list):
        return data[0] if len(data) == 1 else None
    elif isinstance(data, dict):
        return data
    else:
        return None