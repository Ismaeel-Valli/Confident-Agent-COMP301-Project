import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Parameters:
        inputs (dict): Contains:
            - results_to_skip (int): Number of results to skip.
            - excluded_attributes (list): Attributes to exclude from response.
            - credential (str): Caller-supplied credential.
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com/v5"
    endpoint = "/countries"
    
    params = {
        "page": 1,
        "results_to_skip": inputs["results_to_skip"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(base_url + endpoint, params=params, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    
    if not data:
        return None
    
    # Filter out excluded attributes
    if inputs["excluded_attributes"]:
        filtered_data = []
        for country in data:
            filtered_country = {k: v for k, v in country.items() 
                               if k not in inputs["excluded_attributes"]}
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data