import requests

def solve(inputs):
    """
    Look up countries by exact match on their common country name using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): The exact country name to match
            - result_limit (int): Maximum number of results to return
            - credential (str): Caller-supplied API credential
    
    Returns:
        list or None: Decoded JSON response as a list, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build the query parameters
    params = {
        "name": inputs["value"],
        "limit": inputs["result_limit"]
    }
    
    # Make the GET request with credential in header
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(f"{base_url}/v5.0/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data