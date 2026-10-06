import requests

def solve(inputs):
    """
    Look up countries by exact match on their bordering country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Country code to match exactly
            - result_limit: Maximum number of results
            - excluded_attributes: List of attributes to exclude from response
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    excluded_attributes = inputs["excluded_attributes"]
    
    url = "https://api.restcountries.com/v3.1/countries/border"
    params = {
        "code": value,
        "limit": result_limit
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Filter out excluded attributes
    if excluded_attributes:
        filtered_data = {}
        for key, value in data.items():
            if key not in excluded_attributes:
                filtered_data[key] = value
        return filtered_data
    
    return data