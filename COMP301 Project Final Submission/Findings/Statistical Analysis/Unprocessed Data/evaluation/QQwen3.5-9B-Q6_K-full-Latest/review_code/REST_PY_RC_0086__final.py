import requests

def solve(inputs):
    """
    Look up countries by exact match on their region using REST Countries v5 API.
    
    Args:
        inputs (dict): Must contain:
            - "value": The region to match exactly
            - "included_attributes": List of attributes to return for each country
            - "credential": Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response. None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses (non-2xx status codes).
    """
    base_url = "https://api.restcountries.com/v5"
    region = inputs["value"]
    credential = inputs["credential"]
    included_attributes = inputs.get("included_attributes", [])
    
    # Build query parameters
    params = {
        "region": region,
        "credential": credential
    }
    
    if included_attributes:
        params["fields"] = ",".join(included_attributes)
    
    response = requests.get(f"{base_url}/countries", params=params)
    
    # Raise exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    data = response.json()
    
    # Return None for successful empty response, otherwise return the data
    if not data:
        return None
    
    return data