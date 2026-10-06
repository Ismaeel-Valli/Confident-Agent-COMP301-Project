import requests

def solve(inputs):
    """
    Search REST Countries v5 by country codes using a search term.
    
    Args:
        inputs (dict): Must contain:
            - result_limit (int): Maximum number of results to return.
            - search_text (str): The search term to use.
            - credential (str): Caller-supplied authentication token.
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty responses.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://api.restcountries.com"
    search_text = inputs["search_text"]
    result_limit = inputs["result_limit"]
    credential = inputs["credential"]
    
    # Construct the URL with query parameters
    url = f"{base_url}/v5/search?search={search_text}&limit={result_limit}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for empty successful responses
    if not data:
        return None
    
    return data