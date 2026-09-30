import requests

def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - value: Currency code to match exactly
            - result_limit: Maximum number of results
            - included_attributes: List of country attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # REST Countries v5 API endpoint for searching by currency code
    base_url = "https://api.restcountries.com/v5.0"
    url = f"{base_url}/search/currency/{value}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Content-Type": "application/json"
    }
    
    params = {
        "limit": result_limit,
        "fields": ",".join(included_attributes) if included_attributes else None
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (empty list)
    if not data:
        return None
    
    return data