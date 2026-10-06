import requests


def solve(inputs):
    """
    Look up countries by exact currency code match from REST Countries v5.
    
    Args:
        inputs (dict): {
            "value": str - Currency code to match exactly,
            "result_limit": int - Maximum number of results,
            "included_attributes": list[str] - Attributes to include in output,
            "credential": str - Caller-supplied credential with necessary permissions
        }
    
    Returns:
        dict or None - Decoded JSON response (None for successful empty response)
    
    Raises:
        Exception - For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com/v5"
    currency_code = inputs["value"]
    limit = inputs["result_limit"]
    attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    url = f"{base_url}/currency/{currency_code}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    params = {
        "limit": limit,
        "attributes": ",".join(attributes) if attributes else None
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data