import requests

def solve(inputs):
    """
    Look up countries by exact match on their region using REST Countries v5 API.
    
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
    api_url = "https://api.restcountries.com/v5/countries"
    region_value = inputs["value"]
    credential = inputs["credential"]
    included_attributes = inputs.get("included_attributes", [])
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    params = {}
    if region_value:
        params["region"] = region_value
    if included_attributes:
        params["fields"] = ",".join(included_attributes)
    
    response = requests.get(api_url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (empty list)
    if not data:
        return None
    
    return data