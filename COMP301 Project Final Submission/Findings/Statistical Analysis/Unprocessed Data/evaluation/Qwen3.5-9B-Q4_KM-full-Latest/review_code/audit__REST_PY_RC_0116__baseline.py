import requests

def solve(inputs):
    """
    Looks up countries by an exact match on their bordering country code using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The country code to match exactly for borders.
            - 'results_to_skip': Number of results to skip (offset).
            - 'excluded_attributes': List of attributes to exclude from the response.
            - 'credential': Caller-supplied credential (e.g., API key or token).
    
    Returns:
        list or None: Decoded JSON response as a list of countries, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (non-2xx status code).
    """
    
    base_url = "https://restcountries.com/v3.1"
    value = inputs["value"]
    skip = inputs["results_to_skip"]
    excluded_attrs = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Construct the query parameters for bordering country code
    params = {
        "borders": value,  # This will return countries that have 'value' as a border
        "skip": skip,
        "fields": ",".join(excluded_attrs) if excluded_attrs else None
    }
    
    headers = {}
    if credential:
        headers["Authorization"] = f"Bearer {credential}"  # Adjust based on actual auth method required
    
    response = requests.get(f"{base_url}/country", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for a successful empty response
    if not data:
        return None
    
    return data