import requests

def solve(inputs):
    """
    Look up countries by exact match on their bordering country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The bordering country code to match exactly
            - excluded_attributes: List of attributes to exclude from results
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    value = inputs["value"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    credential = inputs["credential"]
    
    # REST Countries v5 API endpoint for a specific country (which includes borders info)
    base_url = "https://api.restcountries.com"
    url = f"{base_url}/v3.1/countries/{value}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # If empty response (country not found), return None
    if not data:
        return None
    
    # Filter out excluded attributes if any
    if excluded_attributes:
        for attr in excluded_attributes:
            if attr in data:
                del data[attr]
    
    return data