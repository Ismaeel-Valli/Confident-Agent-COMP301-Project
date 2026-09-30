import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - result_limit (int): Maximum number of results to return.
            - results_to_skip (int): Number of results to skip (pagination offset).
            - excluded_attributes (list): List of country attributes to exclude.
            - credential (str): Caller-supplied credential with necessary permissions.
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com/v5/countries"
    limit = inputs["result_limit"]
    skip = inputs["results_to_skip"]
    
    # Build query string manually for static analysis
    query_string = f"limit={limit}&skip={skip}"
    url = base_url + "?" + query_string
    
    headers = {
        "Authorization": inputs["credential"]
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If the response is empty (no countries found), return None as per requirement
    if not data:
        return None
    
    # Exclude specified attributes from each country object
    for country in data:
        for attr in inputs["excluded_attributes"]:
            if attr in country:
                del country[attr]
    
    return data