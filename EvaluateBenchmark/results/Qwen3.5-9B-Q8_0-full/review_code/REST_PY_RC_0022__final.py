import requests

def solve(inputs):
    """
    Search country names using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return
            - results_to_skip (int): Number of results to skip
            - search_text (str): Search term for country names
            - credential (str): Caller-supplied API credential
    
    Returns:
        list or None: Decoded JSON response as a list, or None if empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    params = {
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"],
        "searchText": inputs["search_text"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(f"{base_url}/v5/search", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data