import requests

def solve(inputs):
    """
    Look up countries by exact match on their bordering country code using REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - value: Country code to match exactly
            - results_to_skip: Number of results to skip
            - included_attributes: List of attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    value = inputs["value"]
    results_to_skip = inputs["results_to_skip"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    base_url = "https://api.restcountries.com/v5"
    endpoint = f"/country/{value}/borders"
    url = f"{base_url}{endpoint}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    params = {
        "skip": results_to_skip,
        "fields": ",".join(included_attributes) if included_attributes else None
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    return data if data is not None else None