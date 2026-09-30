import requests

def solve(inputs):
    """
    Look up countries by exact match on their common country name using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - "value": The exact country name to search for
            - "credential": Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    value = inputs["value"]
    credential = inputs["credential"]
    
    # Construct the API endpoint for exact match by common name
    url = f"{base_url}/v5.0/country?name={value}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    # Raise exception for unsuccessful HTTP responses
    if not response.ok:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for successful empty response, otherwise return the data
    if not data:
        return None
    
    return data