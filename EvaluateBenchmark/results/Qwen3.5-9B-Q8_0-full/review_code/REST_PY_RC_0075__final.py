import requests

def solve(inputs):
    """
    Look up countries by exact match on their common name using REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - "value": The country name to match exactly
            - "excluded_attributes": List of attributes to exclude from results
            - "credential": Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    """
    base_url = "https://api.restcountries.com"
    value = inputs["value"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "name": value,
        "exclude": ",".join(excluded_attributes) if excluded_attributes else None
    }
    
    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(f"{base_url}/v5.0/countries", params=params, headers=headers)
    
    # Raise exception for unsuccessful HTTP response
    response.raise_for_status()
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data