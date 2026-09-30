import requests


def solve(inputs):
    """
    Look up countries by exact match on their subregion using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Subregion to match exactly
            - result_limit: Maximum number of results
            - results_to_skip: Number of results to skip
            - included_attributes: List of attributes to include in response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com/v5.0"
    endpoint = "/subregion"
    
    params = {
        "value": inputs["value"],
        "result_limit": inputs["result_limit"],
        "results_to_skip": inputs["results_to_skip"],
        "included_attributes": ",".join(inputs["included_attributes"])
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(f"{base_url}{endpoint}", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    return data if data else None