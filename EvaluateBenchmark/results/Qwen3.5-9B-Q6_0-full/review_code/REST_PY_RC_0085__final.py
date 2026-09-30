import requests

def solve(inputs):
    """
    Look up countries by exact region match using REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - value: Region name to match exactly
            - results_to_skip: Number of results to skip (for pagination)
            - credential: Caller-supplied authentication credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com/v5"
    region = inputs["value"]
    skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    url = f"{base_url}/region/{region}"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    params = {
        "skip": skip
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data