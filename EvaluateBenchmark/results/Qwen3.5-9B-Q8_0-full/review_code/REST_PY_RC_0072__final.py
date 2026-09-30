import requests

def solve(inputs):
    """
    Look up countries by exact match on their common country name from REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): The exact country name to match
            - result_limit (int): Maximum number of results to return
            - credential (str): Caller-supplied API credential
    
    Returns:
        list or None: Decoded JSON response as a list, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    credential = inputs["credential"]
    
    url = f"{base_url}/v5/search?name={value}&limit={result_limit}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (empty list)
    if not data:
        return None
    
    return data