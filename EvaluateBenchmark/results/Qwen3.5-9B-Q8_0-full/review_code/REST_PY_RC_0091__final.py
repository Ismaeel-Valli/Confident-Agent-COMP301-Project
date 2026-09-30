import requests

def solve(inputs):
    """
    Look up countries by exact region match using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Region name to match exactly
            - results_to_skip: Number of results to skip (for pagination)
            - included_attributes: List of attributes to include in response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    region = inputs["value"]
    skip = inputs["results_to_skip"]
    attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "region": region,
        "skip": skip
    }
    
    # Add attribute filter if provided
    if attributes:
        params["fields"] = ",".join(attributes)
    
    # Make the request with credential in header
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(f"{base_url}/v5/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data