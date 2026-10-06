import requests

def solve(inputs):
    """
    Looks up countries by an exact match on their subregion using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The subregion value to match exactly.
            - 'result_limit': Maximum number of results to return.
            - 'results_to_skip': Number of results to skip.
            - 'credential': Caller-supplied credential (assumed to have necessary permissions).
    
    Returns:
        list or None: Decoded JSON response as a list, or None if the response is successfully empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    # Construct the API URL with query parameters
    url = "https://restcountries.com/v5.1/subregion"
    params = {
        "subregion": value,
        "limit": result_limit,
        "skip": results_to_skip
    }
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for a successful empty response
    if not data:
        return None
    
    return data