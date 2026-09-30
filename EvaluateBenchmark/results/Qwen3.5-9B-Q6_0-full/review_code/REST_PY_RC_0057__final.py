import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Parameters:
        inputs (dict): Contains:
            - result_limit (int): Maximum number of results to return.
            - results_to_skip (int): Number of results to skip.
            - excluded_attributes (list): Attributes to exclude from the response.
            - credential (str): Caller-supplied credential with necessary permissions.
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    endpoint = "/v5/countries"
    
    params = {
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(base_url + endpoint, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    data = response.json()
    
    # Exclude specified attributes from each country object
    if inputs["excluded_attributes"]:
        for country in data:
            for attr in inputs["excluded_attributes"]:
                if attr in country:
                    del country[attr]
    
    return data if data else None