import requests

def solve(inputs):
    """
    Look up countries by exact match on their two-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Two-letter ISO country code to match exactly
            - results_to_skip (int): Number of results to skip
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    iso_code = inputs["value"]
    skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    # Construct the endpoint for exact match by ISO code
    url = f"{base_url}/v5.0/country/{iso_code}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    # Raise exception for unsuccessful HTTP responses
    if not response.ok:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    # Decode JSON response
    data = response.json()
    
    # Return None for successful empty response
    if data is None or (isinstance(data, dict) and len(data) == 0):
        return None
    
    return data