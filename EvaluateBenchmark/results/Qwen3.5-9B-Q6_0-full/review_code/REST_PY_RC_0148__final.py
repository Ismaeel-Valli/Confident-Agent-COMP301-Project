import requests

def solve(inputs):
    """
    Look up countries by exact match on their capital city using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Capital city name to match exactly
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip
            - credential: Caller-supplied authentication credential
    
    Returns:
        list or None: Decoded JSON response (list of countries) or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com/v5"
    capital = inputs["value"]
    limit = inputs["result_limit"]
    skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    url = f"{base_url}/capital/{capital}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    params = {
        "limit": limit,
        "skip": skip
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (empty list)
    if not data:
        return None
    
    return data