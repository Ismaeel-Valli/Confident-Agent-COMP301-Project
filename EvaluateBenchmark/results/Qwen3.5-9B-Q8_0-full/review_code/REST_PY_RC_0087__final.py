import requests

def solve(inputs):
    """
    Look up countries by exact match on their region using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The region to match exactly
            - excluded_attributes: List of country attributes to exclude from results
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    region = inputs["value"]
    credential = inputs["credential"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    
    # Build query parameters
    params = {
        "region": region,
        "format": "json"
    }
    
    # Add excluded attributes as filters if provided
    if excluded_attributes:
        for attr in excluded_attributes:
            params["exclude"] = attr
    
    # Make the API request with credential
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(f"{base_url}/v5/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response, otherwise return the data
    if not data:
        return None
    
    return data