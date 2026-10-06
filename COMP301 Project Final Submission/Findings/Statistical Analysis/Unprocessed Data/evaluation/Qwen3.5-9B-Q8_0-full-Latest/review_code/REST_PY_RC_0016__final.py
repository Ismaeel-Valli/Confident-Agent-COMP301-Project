import requests

def solve(inputs):
    """
    Look up a country by its two-letter ISO code using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Two-letter ISO country code to match exactly
            - included_attributes (list): List of attributes to return
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    iso_code = inputs["value"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # REST Countries v5 API endpoint for exact match by ISO code
    base_url = "https://api.restcountries.com"
    url = f"{base_url}/v5.2/country/{iso_code}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If the country is not found, the API returns an empty object or similar
    # We return None for a successful empty response (country not found)
    if not data or (isinstance(data, dict) and len(data) == 0):
        return None
    
    # Filter the response to include only the requested attributes
    if included_attributes:
        filtered_data = {}
        for attr in included_attributes:
            if attr in data:
                filtered_data[attr] = data[attr]
        return filtered_data
    
    return data