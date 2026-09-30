import requests

def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Currency code to match exactly
            - result_limit: Maximum number of results
            - included_attributes: List of attributes to return for each country
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # REST Countries v5 API endpoint for filtering by currency code
    base_url = "https://api.restcountries.com"
    url = f"{base_url}/v5.1/countries?currency={value}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    params = {
        "limit": result_limit,
        "attributes": ",".join(included_attributes) if included_attributes else None
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (no countries found)
    if not data:
        return None
    
    return data