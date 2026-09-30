import requests

def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Currency code to match exactly
            - excluded_attributes (list): Attributes to exclude from results
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response. None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com/v5"
    currency_code = inputs["value"]
    credential = inputs["credential"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    
    # Build query parameters
    params = {
        "currency": currency_code,
        "exclude": ",".join(excluded_attributes) if excluded_attributes else None
    }
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(base_url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data