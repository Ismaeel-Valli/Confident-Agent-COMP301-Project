import requests

def solve(inputs):
    """
    Look up countries by exact match on their capital city using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Capital city to match exactly
            - results_to_skip (int): Number of results to skip
            - credential (str): Caller-supplied authentication credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    capital = inputs["value"]
    skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    # REST Countries v5 uses /v5/capitals endpoint with query parameter for name
    url = f"{base_url}/v5/capitals?name={capital}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If the response is empty (no countries found), return None
    if not data or len(data) == 0:
        return None
    
    # Apply pagination (skip results)
    if skip > 0 and isinstance(data, list):
        paginated_data = data[skip:]
        return paginated_data
    
    return data