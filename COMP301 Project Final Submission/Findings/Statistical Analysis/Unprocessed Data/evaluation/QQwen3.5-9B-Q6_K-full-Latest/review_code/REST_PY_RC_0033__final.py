import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - result_limit (int): Maximum number of results to return
            - excluded_attributes (list): Attributes to exclude from response
            - credential (str): Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    endpoint = "/v5.0/countries"
    
    # Build query parameters
    params = {
        "limit": inputs["result_limit"]
    }
    
    # Make the API request with credential in header
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(base_url + endpoint, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If empty response, return None
    if not data:
        return None
    
    # Filter out excluded attributes
    if inputs["excluded_attributes"]:
        for country in data:
            for attr in inputs["excluded_attributes"]:
                if attr in country:
                    del country[attr]
    
    return data