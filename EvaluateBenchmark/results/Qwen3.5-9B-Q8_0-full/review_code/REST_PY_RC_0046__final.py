import requests

def solve(inputs):
    """
    Search country names using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - results_to_skip (int): Number of results to skip.
            - excluded_attributes (list): List of attributes to exclude from results.
            - search_text (str): Search term for country names.
            - credential (str): Caller-supplied credential (assumed valid).
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
    
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    base_url = "https://api.restcountries.com"
    endpoint = "/v5/search/name"
    
    params = {
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"],
        "searchText": inputs["search_text"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(
        base_url + endpoint,
        params=params,
        headers=headers
    )
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Filter out excluded attributes if any
    if inputs["excluded_attributes"]:
        filtered_data = []
        for country in data:
            filtered_country = {}
            for key, value in country.items():
                if key not in inputs["excluded_attributes"]:
                    filtered_country[key] = value
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data