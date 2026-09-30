import requests

def solve(inputs):
    """
    Look up countries by exact match on their bordering country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Country code to match exactly (bordering country)
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip
            - credential: Caller-supplied authentication credential
    
    Returns:
        list or None: Decoded JSON response as a list, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    base_url = "https://api.restcountries.com"
    endpoint = f"/v5/countries/borders/{value}"
    url = f"{base_url}{endpoint}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    params = {
        "limit": result_limit,
        "skip": results_to_skip
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data