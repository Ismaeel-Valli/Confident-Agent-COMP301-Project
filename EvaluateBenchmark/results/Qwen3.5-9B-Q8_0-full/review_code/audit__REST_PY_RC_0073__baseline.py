import requests

def solve(inputs):
    """
    Looks up countries by exact match on their common country name using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The exact country name to search for.
            - 'results_to_skip': Number of results to skip (for pagination).
            - 'credential': Caller-supplied credential (assumed to have necessary permissions).
    
    Returns:
        list or None: Decoded JSON response as a list of countries, or None if the response is empty but successful.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://restcountries.com/v5.1/data"
    value = inputs["value"]
    results_to_skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    # Construct the URL with query parameters
    url = f"{base_url}/{value}"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP request failed with status code: {response.status_code}")
    
    data = response.json()
    
    # If the response is an empty list, return None as per requirement
    if not data:
        return None
    
    return data