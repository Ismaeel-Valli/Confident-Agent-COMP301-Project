import requests

def solve(inputs):
    """
    Looks up countries by an exact match on their common country name using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The exact country name to search for.
            - 'results_to_skip': Number of results to skip.
            - 'credential': Caller-supplied credential (assumed to have necessary permissions).
    
    Returns:
        list or None: Decoded JSON response as a list of countries, or None if the response is empty but successful.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    value = inputs["value"]
    results_to_skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    # Construct the API URL with query parameters for exact match and skip
    url = f"https://restcountries.com/v3.1/name/{value}?skip={results_to_skip}"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP request failed with status code: {response.status_code}")
    
    data = response.json()
    
    # Return None for a successful empty response
    if not data:
        return None
    
    return data