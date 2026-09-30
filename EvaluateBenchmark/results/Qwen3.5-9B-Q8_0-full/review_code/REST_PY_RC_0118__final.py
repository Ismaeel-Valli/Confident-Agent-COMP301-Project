import requests

def solve(inputs):
    """
    Look up countries by an exact match on their bordering country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Country code to match exactly in borders
            - result_limit (int): Maximum number of results
            - results_to_skip (int): Number of results to skip
            - excluded_attributes (list): Attributes to exclude from response
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build query parameters
    params = {
        "border": inputs["value"],
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"]
    }
    
    # Make the request with credential in header
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(
        base_url,
        params=params,
        headers=headers
    )
    
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