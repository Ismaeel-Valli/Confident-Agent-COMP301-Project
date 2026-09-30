import requests

def solve(inputs):
    """
    Looks up countries by exact match on their common country name using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The exact country name to search for.
            - 'included_attributes': List of attributes to include in the response.
            - 'credential': Authentication token/credential for the API.
    
    Returns:
        dict or None: Decoded JSON response if found, None if no results found (successful empty response).
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    value = inputs["value"]
    included_attributes = inputs.get("included_attributes", [])
    credential = inputs["credential"]
    
    # Construct the URL with query parameters
    url = "https://restcountries.com/v3.1/name"
    params = {
        "name": value,
        "fields": ",".join(included_attributes) if included_attributes else None
    }
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    data = response.json()
    
    # If the response is a list and empty, return None
    if isinstance(data, list) and len(data) == 0:
        return None
    
    return data