import requests

def solve(inputs):
    """
    Look up countries by exact match on their two-letter ISO country code.
    
    Args:
        inputs (dict): {
            "value": str - The two-letter ISO country code to match exactly,
            "result_limit": int - Maximum number of results,
            "credential": str - Caller-supplied credential with necessary permissions
        }
    
    Returns:
        list or None - Decoded JSON response (list of countries) or None for empty response
    
    Raises:
        Exception - For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    country_code = inputs["value"]
    result_limit = inputs["result_limit"]
    credential = inputs["credential"]
    
    url = f"{base_url}/v5.0/country/{country_code}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response, otherwise return the data
    if not data:
        return None
    
    return data