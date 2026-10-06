import requests

def solve(inputs):
    """
    Look up countries by exact match on their common country name using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The exact country name to search for
            - results_to_skip: Number of results to skip (for pagination)
            - included_attributes: List of attributes to include in the response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty
        Raises: Exception for unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build query parameters
    params = {
        "name": inputs["value"],
        "skip": inputs["results_to_skip"],
        "fields": ",".join(inputs["included_attributes"])
    }
    
    # Make the API request with credential
    headers = {"Authorization": f"Bearer {inputs['credential']}"}
    response = requests.get(f"{base_url}/v5/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data