import requests

def solve(inputs):
    """
    Look up countries by exact match on their bordering country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Country code to match exactly (str)
            - result_limit: Maximum number of results (int)
            - results_to_skip: Number of results to skip (int)
            - included_attributes: List of attributes to return (list)
            - credential: Caller-supplied credential (str)
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com/v5"
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    url = f"{base_url}/countries?borders={value}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    params = {
        "limit": result_limit,
        "skip": results_to_skip
    }
    
    if included_attributes:
        params["attributes"] = ",".join(included_attributes)
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    return data if data is not None else None