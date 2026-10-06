import requests

def solve(inputs):
    """
    Look up a country by its three-letter ISO code using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Three-letter ISO country code to match exactly
            - included_attributes (list): List of attributes to include in response
            - credential (str): Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    iso_code = inputs["value"]
    included_attrs = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "iso3": iso_code,
        "fields": ",".join(included_attrs) if included_attrs else "",
        "key": credential
    }
    
    response = requests.get(f"{base_url}/v5.0/country", params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}, {response.text}")
    
    data = response.json()
    
    # REST Countries v5 returns a list of countries or an empty list
    if not data:
        return None
    
    return data