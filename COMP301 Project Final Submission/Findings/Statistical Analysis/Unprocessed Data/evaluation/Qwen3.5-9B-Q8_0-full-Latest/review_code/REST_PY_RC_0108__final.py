import requests

def solve(inputs):
    """
    Look up countries by an exact match on their bordering country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Country code to match exactly in borders
            - result_limit (int): Maximum number of results to return
            - credential (str): Caller-supplied API credential
    
    Returns:
        dict or None: Decoded JSON response, or None if empty but successful
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    credential = inputs["credential"]
    
    url = f"{base_url}/v3.1/all"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Filter countries that have the specified bordering country code
    result = []
    if isinstance(data, dict) and "data" in data:
        for country in data["data"]:
            borders = country.get("borders", [])
            if value in borders:
                result.append(country)
    
    # Apply result limit
    result = result[:result_limit]
    
    return result