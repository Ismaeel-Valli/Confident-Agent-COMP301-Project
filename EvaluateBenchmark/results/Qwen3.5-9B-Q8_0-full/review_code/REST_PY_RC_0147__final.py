import requests

def solve(inputs):
    """
    Look up countries by exact match on their capital city using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The capital city to match exactly
            - excluded_attributes: List of country attributes to exclude from results
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com/v5"
    capital = inputs["value"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    credential = inputs["credential"]
    
    # Build query parameters for exact match on capital
    params = {
        "capital": capital,
        "exclude": ",".join(excluded_attributes) if excluded_attributes else ""
    }
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(f"{base_url}/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data