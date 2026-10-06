import requests

def solve(inputs):
    """
    Looks up countries by an exact match on their two-letter ISO country code using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The two-letter ISO country code to match exactly.
            - 'result_limit': Maximum number of results to return.
            - 'included_attributes': List of attributes to include in the response.
            - 'credential': API credential for authentication.
    
    Returns:
        dict or None: Decoded JSON response if successful, or None if the response is empty but successful.
        Raises:
            Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://restcountries.com/v5.1"
    country_code = inputs["value"]
    result_limit = inputs["result_limit"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Construct the URL with query parameters
    url = f"{base_url}/country/{country_code}"
    
    # Prepare headers with the credential
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    params = {
        "limit": result_limit,
        "fields": ",".join(included_attributes) if included_attributes else None
    }
    
    # Make the GET request
    response = requests.get(url, headers=headers, params=params)
    
    # Check for unsuccessful HTTP response
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code} error: {response.text}")
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for a successful empty response
    if not data:
        return None
    
    return data