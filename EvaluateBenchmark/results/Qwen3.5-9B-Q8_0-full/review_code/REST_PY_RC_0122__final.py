import requests

def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The currency code to match exactly
            - included_attributes: List of country attributes to return
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    value = inputs["value"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    base_url = "https://api.restcountries.com"
    url = f"{base_url}/v5/currency/{value}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Filter to only include requested attributes if specified
    if included_attributes and isinstance(included_attributes, list):
        filtered_data = {}
        for attr in included_attributes:
            if attr in data:
                filtered_data[attr] = data[attr]
        return filtered_data
    
    return data