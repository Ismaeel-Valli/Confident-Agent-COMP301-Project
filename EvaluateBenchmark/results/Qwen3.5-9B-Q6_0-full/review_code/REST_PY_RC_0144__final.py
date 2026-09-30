import requests

def solve(inputs):
    """
    Look up countries by exact match on their capital city using REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - value: The capital city to match exactly
            - result_limit: Maximum number of results to return
            - credential: Caller-supplied authentication credential
    
    Returns:
        list or None: Decoded JSON response, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    credential = inputs["credential"]
    
    # REST Countries v5 API endpoint for searching by capital
    base_url = "https://api.restcountries.com/v5.0"
    url = f"{base_url}/search/capital/{value}"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Apply result limit
    if isinstance(data, list):
        return data[:result_limit]
    elif isinstance(data, dict) and "data" in data:
        return data["data"][:result_limit]
    else:
        return None