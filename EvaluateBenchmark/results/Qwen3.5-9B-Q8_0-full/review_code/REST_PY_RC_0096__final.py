import requests

def solve(inputs):
    """
    Look up countries by exact match on their subregion using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The subregion to match exactly
            - result_limit: Maximum number of results to return
            - credential: Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    subregion = inputs["value"]
    limit = inputs["result_limit"]
    credential = inputs["credential"]
    
    url = f"{base_url}/v5/countries?subregions={subregion}&limit={limit}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # REST Countries v5 returns an empty list for no matches, not null
    # The spec says return None for successful empty response, so we interpret that as:
    # if the API returns an empty list (no countries found), return None
    if data == []:
        return None
    
    return data