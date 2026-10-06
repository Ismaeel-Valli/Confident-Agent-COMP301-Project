import requests

def solve(inputs):
    """
    Looks up countries by exact match on their common country name using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The exact country name to search for.
            - 'included_attributes': List of attributes to include in the response.
            - 'credential': API key/credential for authentication.
    
    Returns:
        dict or None: Decoded JSON response if found, None if no results found.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not 200).
    """
    value = inputs["value"]
    included_attributes = inputs.get("included_attributes", [])
    credential = inputs["credential"]
    
    # Construct the query string for exact match on common name
    params = {
        "name": value,
        "includemeasures": ",".join(included_attributes) if included_attributes else None
    }
    
    url = "https://restcountries.com/v3.1/name"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If the list is empty, return None as per requirement for successful empty response
    if not data:
        return None
    
    return data