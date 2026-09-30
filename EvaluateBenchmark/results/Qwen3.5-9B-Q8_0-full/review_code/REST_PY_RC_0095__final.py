import requests

def solve(inputs):
    """
    Look up countries by exact match on their subregion using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - "value": The subregion to match exactly
            - "credential": Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    value = inputs["value"]
    credential = inputs["credential"]
    
    # REST Countries v5 API endpoint for subregion query
    url = "https://api.restcountries.com/v5.0/subregions"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    params = {
        "subregion": value
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (empty list or empty dict)
    if not data:
        return None
    
    return data