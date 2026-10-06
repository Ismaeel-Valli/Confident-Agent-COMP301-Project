import requests

def solve(inputs):
    """
    Look up countries by exact currency code match using REST Countries v5 API.
    
    Args:
        inputs (dict): Must contain:
            - value: Currency code to match exactly
            - results_to_skip: Number of results to skip
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    value = inputs["value"]
    results_to_skip = inputs["results_to_skip"]
    
    base_url = "https://api.restcountries.com/v5"
    url = f"{base_url}/currency/{value}"
    
    params = {
        "skip": results_to_skip
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    return data if data else None