import requests


def solve(inputs):
    """
    Look up countries by exact match on their bordering country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Country code to match exactly against bordering countries
            - result_limit: Maximum number of results to return
            - included_attributes: List of attributes to include in the response
            - credential: Caller-supplied credential for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty
        Raises: Exception for unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build query parameters
    params = {
        "border": inputs["value"],
        "limit": inputs["result_limit"],
        "fields": ",".join(inputs["included_attributes"])
    }
    
    # Make the API request with provided credential
    headers = {"Authorization": f"Bearer {inputs['credential']}"}
    response = requests.get(f"{base_url}/v5/country", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data