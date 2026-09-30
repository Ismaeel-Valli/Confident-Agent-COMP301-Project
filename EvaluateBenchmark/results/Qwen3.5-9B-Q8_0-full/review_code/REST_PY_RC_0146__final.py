import requests

def solve(inputs):
    """
    Look up countries by exact match on their capital city using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The capital city to match exactly
            - included_attributes: List of country attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    capital = inputs["value"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build the query parameters for exact match on capital
    params = {
        "capital": capital,
        "fields": ",".join(included_attributes) if included_attributes else None
    }
    
    # Make the API request with credentials in headers
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(base_url, params=params, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for successful empty response (empty list)
    if not data:
        return None
    
    return data