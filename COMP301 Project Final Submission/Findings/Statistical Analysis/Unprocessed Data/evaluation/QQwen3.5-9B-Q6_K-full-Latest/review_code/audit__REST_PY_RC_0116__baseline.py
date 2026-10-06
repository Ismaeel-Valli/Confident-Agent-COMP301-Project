import requests

def solve(inputs):
    """
    Looks up countries by an exact match on their bordering country code using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The country code to match exactly for borders.
            - 'results_to_skip': Number of results to skip (offset).
            - 'excluded_attributes': List of attributes to exclude from the response.
            - 'credential': API credential/token.
    
    Returns:
        list or None: Decoded JSON response as a list, or None if the response is empty but successful.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not in 200-299).
    """
    value = inputs['value']
    results_to_skip = inputs['results_to_skip']
    excluded_attributes = inputs['excluded_attributes']
    credential = inputs['credential']
    
    # Base URL for REST Countries v5 API
    base_url = "https://restcountries.com/v3.1"
    
    # Construct the query parameters
    params = {
        'borders': value,  # Match countries that border the given country code
        'skip': results_to_skip,
        'exclude': ','.join(excluded_attributes) if excluded_attributes else None
    }
    
    # Remove None values from params to avoid sending them in the URL
    params = {k: v for k, v in params.items() if v is not None}
    
    headers = {
        'Authorization': f'Bearer {credential}'
    }
    
    response = requests.get(f"{base_url}/country", params=params, headers=headers)
    
    # Check if the HTTP response was successful
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for a successful empty response
    if not data:
        return None
    
    return data