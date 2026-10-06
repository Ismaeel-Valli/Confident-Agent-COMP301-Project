import requests

def solve(inputs):
    """
    Look up countries by exact match on their region using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Region name to match exactly
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip (pagination)
            - included_attributes: List of attributes to include in response
            - credential: Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response as a list, or None for empty successful response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    region = inputs["value"]
    limit = inputs["result_limit"]
    skip = inputs["results_to_skip"]
    attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "region": region,
        "limit": limit,
        "skip": skip,
        "fields": ",".join(attributes) if attributes else None
    }
    
    # Remove None fields from params
    params = {k: v for k, v in params.items() if v is not None}
    
    url = f"{base_url}/v5/countries"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data