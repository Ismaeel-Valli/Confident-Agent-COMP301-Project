import requests

def solve(inputs):
    """
    Look up countries by exact match on their region using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The region to match exactly
            - included_attributes: List of attributes to return for each country
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com/v3.1"
    region = inputs["value"]
    credential = inputs["credential"]
    included_attributes = inputs.get("included_attributes", [])
    
    # Build query parameters
    params = {
        "region": region,
        "format": "json"
    }
    
    if included_attributes:
        params["fields"] = ",".join(included_attributes)
    
    # Make the request with credential in headers
    headers = {"Authorization": f"Bearer {credential}"}
    
    response = requests.get(base_url, params=params, headers=headers)
    
    # Raise exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode JSON response
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data