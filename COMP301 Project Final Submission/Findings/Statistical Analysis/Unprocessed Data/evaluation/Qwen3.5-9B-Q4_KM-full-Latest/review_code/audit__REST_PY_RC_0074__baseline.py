import requests

def solve(inputs):
    """
    Looks up countries by an exact match on their common country name using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The exact country name to search for.
            - 'included_attributes': List of attributes to include in the response.
            - 'credential': Authentication token/credential for the API request.
    
    Returns:
        dict or None: Decoded JSON response if found, or None if no countries match.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (non-2xx status code).
    """
    value = inputs.get("value")
    included_attributes = inputs.get("included_attributes", [])
    credential = inputs.get("credential")
    
    # Construct the API URL with query parameters
    url = "https://restcountries.com/v3.1/name"
    params = {
        "name": value,
        "fields": ",".join(included_attributes) if included_attributes else None
    }
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        # REST Countries v3.1 returns a list; if no match, it's an empty list
        return data if data else None
    elif response.status_code == 404:
        # Not found is treated as successful empty response per instructions
        return None
    else:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")