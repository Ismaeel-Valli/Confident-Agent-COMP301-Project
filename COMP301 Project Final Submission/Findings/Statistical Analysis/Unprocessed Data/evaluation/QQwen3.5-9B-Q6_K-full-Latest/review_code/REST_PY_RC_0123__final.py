import requests

def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Currency code to match exactly
            - excluded_attributes: List of country attributes to exclude from results
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    # Base URL for REST Countries v5 API
    base_url = "https://api.restcountries.com/v5"
    
    # Build the query parameters
    params = {
        'currency': inputs['value']
    }
    
    # Make the API request with the provided credential
    response = requests.get(base_url, params=params, headers={'Authorization': f'Bearer {inputs["credential"]}'} if inputs.get('credential') else {})
    
    # Check for unsuccessful HTTP response
    if not response.ok:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for successful empty response, otherwise return the data
    if not data:
        return None
    
    return data