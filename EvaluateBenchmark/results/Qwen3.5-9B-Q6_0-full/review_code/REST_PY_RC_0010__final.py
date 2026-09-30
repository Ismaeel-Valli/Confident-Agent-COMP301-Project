import requests

def solve(inputs):
    """
    Search country names on REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - results_to_skip (int): Number of results to skip (offset)
            - search_text (str): Search term for country names
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    search_text = inputs["search_text"]
    results_to_skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    # Build the URL with query parameters
    url = f"{base_url}/v5/search?name={search_text}&skip={results_to_skip}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data