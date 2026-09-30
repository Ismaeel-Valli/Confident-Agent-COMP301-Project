import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Parameters:
        inputs (dict): Contains:
            - result_limit (int): Maximum number of results to return.
            - excluded_attributes (list): Attributes to exclude from the response.
            - credential (str): Caller-supplied credential with necessary permissions.
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    endpoint = "/v5/countries"
    
    params = {
        "limit": inputs["result_limit"]
    }
    
    headers = {}
    
    response = requests.get(f"{base_url}{endpoint}", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Filter out excluded attributes if any
    if inputs["excluded_attributes"]:
        filtered_data = []
        for country in data:
            filtered_country = {}
            for k, v in country.items():
                if k not in inputs["excluded_attributes"]:
                    filtered_country[k] = v
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data