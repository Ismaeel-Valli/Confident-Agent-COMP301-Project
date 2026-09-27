def solve(inputs):
    """
    Look up countries by exact match on their bordering country code using REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - value: Country code to match exactly for borders
            - results_to_skip: Number of results to skip
            - excluded_attributes: List of attributes to exclude from response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None if successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    base_url = "https://api.restcountries.com/v5"
    endpoint = "/country/borders/{code}"
    
    url = base_url + endpoint.replace("{code}", inputs["value"])
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    # Skip results if needed
    if inputs["results_to_skip"] > 0:
        if isinstance(data, list):
            data = data[inputs["results_to_skip"]:]
        elif isinstance(data, dict):
            pass
    
    # Exclude attributes if needed
    if inputs["excluded_attributes"]:
        if isinstance(data, list):
            data = [dict(item) for item in data]
            for item in data:
                for attr in inputs["excluded_attributes"]:
                    if attr in item:
                        del item[attr]
        elif isinstance(data, dict):
            for attr in inputs["excluded_attributes"]:
                if attr in data:
                    del data[attr]
    
    return data