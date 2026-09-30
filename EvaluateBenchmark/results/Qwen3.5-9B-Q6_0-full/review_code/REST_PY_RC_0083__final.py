import requests

def solve(inputs):
    """
    Look up countries by exact match on their region using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - "value": The region value to match exactly
            - "credential": Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    api_url = "https://api.restcountries.com/v5/countries"
    
    # Prepare the request parameters
    params = {
        "region": inputs["value"]
    }
    
    # Make the GET request with credentials in headers
    response = requests.get(api_url, params=params, headers={
        "Authorization": f"Bearer {inputs['credential']}"
    })
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data