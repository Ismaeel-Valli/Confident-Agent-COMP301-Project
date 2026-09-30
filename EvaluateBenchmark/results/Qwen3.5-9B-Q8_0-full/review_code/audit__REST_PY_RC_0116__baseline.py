import requests

def solve(inputs):
    """
    Looks up countries by an exact match on their bordering country code using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The country code to match exactly for borders.
            - 'results_to_skip': Number of results to skip (offset).
            - 'excluded_attributes': List of attributes to exclude from the response.
            - 'credential': Caller-supplied credential (API key/token).
    
    Returns:
        dict or None: Decoded JSON response if successful, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    value = inputs["value"]
    results_to_skip = inputs["results_to_skip"]
    excluded_attributes = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Construct the query string for filtering by bordering country code
    params = {
        "border": value,
        "skip": results_to_skip,
        "exclude": ",".join(excluded_attributes) if excluded_attributes else None
    }
    
    url = "https://restcountries.com/v3.1/all"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP request failed with status code: {response.status_code}")
    
    data = response.json()
    
    # Return None for a successful empty response
    if not data:
        return None
    
    return data