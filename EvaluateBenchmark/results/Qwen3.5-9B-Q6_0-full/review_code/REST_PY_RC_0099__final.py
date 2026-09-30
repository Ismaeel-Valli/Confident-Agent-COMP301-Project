import requests

def solve(inputs):
    """
    Look up countries by exact match on their subregion using REST Countries API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The subregion to match exactly
            - excluded_attributes: List of attributes to exclude from results
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    subregion = inputs["value"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "subregion": subregion,
        "exclude": ",".join(excluded_attributes) if excluded_attributes else None
    }
    
    # Make the API request with credentials in headers
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(f"{base_url}/v3", params=params, headers=headers)
    
    # Raise exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode JSON response
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data