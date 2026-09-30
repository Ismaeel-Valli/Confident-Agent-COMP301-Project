import requests

def solve(inputs):
    """
    Look up countries by exact match on their capital city using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The capital city to match exactly
            - included_attributes: List of attributes to return for each country
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    capital = inputs["value"]
    attributes = inputs.get("included_attributes", [])
    credential = inputs["credential"]
    
    # Build the API URL with query parameters
    base_url = "https://api.restcountries.com/v5"
    params = {
        "capital": capital,
        "fields": ",".join(attributes) if attributes else None
    }
    
    # Make the request with credential in header
    headers = {"Authorization": f"Bearer {credential}"}
    
    response = requests.get(base_url, params=params, headers=headers)
    
    # Raise exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode JSON response
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data