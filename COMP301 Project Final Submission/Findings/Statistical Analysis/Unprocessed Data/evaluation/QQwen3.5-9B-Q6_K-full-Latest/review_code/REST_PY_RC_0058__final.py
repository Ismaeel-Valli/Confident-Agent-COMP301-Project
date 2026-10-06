import requests

def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): {
            "value": str - The three-letter ISO country code to match exactly,
            "excluded_attributes": list of str - Attributes to exclude from results,
            "credential": str - Caller-supplied credential with necessary permissions
        }
    
    Returns:
        dict or None - Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception - For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    iso_code = inputs["value"]
    excluded_attrs = inputs.get("excluded_attributes", [])
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "iso3": iso_code,
        "fields": ",".join(excluded_attrs) if excluded_attrs else None,
        "crd": credential
    }
    
    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}
    
    response = requests.get(f"{base_url}/v5.0/countries", params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data