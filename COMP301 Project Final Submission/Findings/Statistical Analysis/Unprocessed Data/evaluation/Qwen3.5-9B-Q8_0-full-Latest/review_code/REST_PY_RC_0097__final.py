import requests

def solve(inputs):
    """
    Look up countries by exact subregion match using REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - value: The exact subregion to match
            - results_to_skip: Number of results to skip (for pagination)
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    subregion = inputs["value"]
    skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    # REST Countries v5 uses /v5/countries endpoint with query parameters
    url = f"{base_url}/v5/countries?subregion={subregion}&skip={skip}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (empty list or null)
    if data is None or len(data) == 0:
        return None
    
    return data