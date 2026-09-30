import requests

def solve(inputs):
    """
    Look up countries by exact match on their bordering country code using REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - value: The country code to match exactly as a bordering country
            - results_to_skip: Number of results to skip (pagination)
            - included_attributes: List of attributes to include in the response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    value = inputs["value"]
    results_to_skip = inputs["results_to_skip"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build the query parameters
    params = {
        "border": value,
        "skip": results_to_skip,
        "fields": ",".join(included_attributes)
    }
    
    # Make the request with the provided credential
    headers = {"Authorization": f"Bearer {credential}"}
    response = requests.get(f"{base_url}/v5/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}, {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data