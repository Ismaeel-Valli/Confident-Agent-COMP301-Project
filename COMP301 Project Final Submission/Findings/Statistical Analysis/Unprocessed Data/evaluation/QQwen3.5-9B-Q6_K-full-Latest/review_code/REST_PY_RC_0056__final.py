import requests

def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Must contain:
            - "value": The three-letter ISO country code to match exactly.
            - "included_attributes": List of attributes to return.
            - "credential": Caller-supplied credential with necessary permissions.
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    iso_code = inputs["value"]
    credential = inputs["credential"]
    included_attributes = inputs.get("included_attributes", [])
    
    # Build the request URL with query parameters
    params = {
        "iso3": iso_code,
        "fields": ",".join(included_attributes) if included_attributes else None
    }
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(
        base_url + "/v5/country",
        params=params,
        headers=headers
    )
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data