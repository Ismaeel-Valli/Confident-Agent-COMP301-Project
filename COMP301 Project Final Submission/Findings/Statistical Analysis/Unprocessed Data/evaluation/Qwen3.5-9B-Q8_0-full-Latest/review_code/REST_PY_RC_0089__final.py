import requests

def solve(inputs):
    """
    Look up countries by exact match on their region using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The region to match exactly
            - result_limit: Maximum number of results
            - included_attributes: List of attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response, or None for empty successful response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    region = inputs["value"]
    limit = inputs["result_limit"]
    attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "region": region,
        "limit": limit,
        "fields": ",".join(attributes)
    }
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(f"{base_url}/v5/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data