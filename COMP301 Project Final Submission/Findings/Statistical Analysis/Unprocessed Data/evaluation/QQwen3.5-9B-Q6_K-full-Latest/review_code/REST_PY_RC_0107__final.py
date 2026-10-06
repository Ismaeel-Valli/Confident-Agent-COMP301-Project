import requests

def solve(inputs):
    """
    Look up countries by an exact match on their bordering country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - "value": The country code to match exactly against borders
            - "credential": Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    value = inputs["value"]
    credential = inputs["credential"]
    
    # REST Countries v5 API endpoint for bordering countries
    url = f"https://api.restcountries.com/v3.1/countries/{value}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response, otherwise return the data
    if not data:
        return None
    
    return data