import requests


def solve(inputs):
    """
    Look up countries by exact match on common name using REST Countries v5.
    
    Args:
        inputs (dict): {
            "value": str - exact country name to match,
            "result_limit": int - max number of results,
            "included_attributes": list[str] - attributes to return,
            "credential": str - caller-supplied credential
        }
    
    Returns:
        dict or None - decoded JSON response (None for empty success)
    
    Raises:
        Exception - on unsuccessful HTTP response
    """
    base_url = "https://api.restcountries.com"
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    params = {
        "name": value,
        "limit": result_limit,
        "fields": ",".join(included_attributes)
    }
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(base_url + "/v5/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    return response.json()