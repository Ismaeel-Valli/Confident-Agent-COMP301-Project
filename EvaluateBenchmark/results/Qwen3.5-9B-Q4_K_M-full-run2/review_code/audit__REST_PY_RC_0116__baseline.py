import requests

def solve(inputs):
    """
    Looks up countries by an exact match on their bordering country code using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The country code to match exactly for borders.
            - 'results_to_skip': Number of results to skip (offset).
            - 'excluded_attributes': List of attributes to exclude from the response.
            - 'credential': API credential/token for authentication.
    
    Returns:
        list or None: Decoded JSON response as a list, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not in 2xx range).
    """
    value = inputs.get('value')
    results_to_skip = inputs.get('results_to_skip', 0)
    excluded_attributes = inputs.get('excluded_attributes', [])
    credential = inputs.get('credential')
    
    # Construct the query parameters for REST Countries v5 API
    params = {
        'border': value,
        'skip': results_to_skip,
        'exclude': ','.join(excluded_attributes) if excluded_attributes else None
    }
    
    # Remove None values from params to avoid sending unnecessary parameters
    params = {k: v for k, v in params.items() if v is not None}
    
    url = "https://restcountries.com/v3.1"
    
    headers = {
        'Authorization': f'Bearer {credential}'
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"HTTP Error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for a successful empty response
    if not data:
        return None
    
    return data