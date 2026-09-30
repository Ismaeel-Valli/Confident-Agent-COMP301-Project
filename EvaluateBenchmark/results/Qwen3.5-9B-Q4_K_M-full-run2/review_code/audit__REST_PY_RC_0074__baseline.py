import requests

def solve(inputs):
    """
    Looks up countries by an exact match on their common country name using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The exact country name to search for.
            - 'included_attributes': A list of attributes to include in the response.
            - 'credential': The caller-supplied credential (e.g., API key or token).
    
    Returns:
        dict or None: The decoded JSON response if found, or None if no country is found.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (non-2xx status code).
    """
    value = inputs["value"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Construct the query parameters
    params = {
        "q": value,
        "fields": ",".join(included_attributes) if included_attributes else None
    }
    
    # Make the API request
    url = "https://restcountries.com/v3.1"
    headers = {"Authorization": f"Bearer {credential}"} if credential else {}
    
    response = requests.get(url, params=params, headers=headers)
    
    # Check for unsuccessful HTTP response
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    # Return None if the response is empty (no country found), otherwise return the data
    if not data:
        return None
    
    return data