import requests

def solve(inputs):
    """
    Look up countries by an exact match on their two-letter ISO country code using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The two-letter ISO country code to match exactly.
            - 'result_limit': Maximum number of results to return.
            - 'included_attributes': List of attributes to include in the response.
            - 'credential': API credential/token for authentication.
    
    Returns:
        list or None: Decoded JSON response as a list of country objects, or None if empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (non-2xx status code).
    """
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Construct query parameters
    params = {
        "q": value,
        "limit": result_limit,
        "fields": ",".join(included_attributes) if included_attributes else None
    }
    
    # Remove 'None' fields from params to avoid sending them in the URL
    params = {k: v for k, v in params.items() if v is not None}
    
    url = "https://restcountries.com/v3.1"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP Error: Status code {response.status_code}, Response: {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data