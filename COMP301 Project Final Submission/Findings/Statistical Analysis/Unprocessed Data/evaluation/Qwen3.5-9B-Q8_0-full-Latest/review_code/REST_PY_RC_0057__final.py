import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - result_limit (int): Maximum number of results to return.
            - results_to_skip (int): Number of results to skip.
            - excluded_attributes (list): Attributes to exclude from response.
            - credential (str): Caller-supplied credential for authentication.
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com/v5/countries"
    params = {
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(base_url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Filter out excluded attributes if any
    if inputs["excluded_attributes"]:
        filtered_data = {}
        for key, value in data.items():
            if key not in inputs["excluded_attributes"]:
                filtered_data[key] = value
        return filtered_data
    
    return data