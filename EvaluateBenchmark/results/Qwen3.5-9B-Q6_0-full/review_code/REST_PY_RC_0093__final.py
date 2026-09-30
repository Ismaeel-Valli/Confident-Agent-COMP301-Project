import requests


def solve(inputs):
    """
    Look up countries by exact region match from REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - value (str): Region to match exactly
            - result_limit (int): Maximum number of results
            - results_to_skip (int): Number of results to skip
            - included_attributes (list[str]): Attributes to include in response
            - credential (str): API key/credential
    
    Returns:
        list or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com/v5"
    
    params = {
        "region": inputs["value"],
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(
        f"{base_url}/countries",
        params=params,
        headers=headers
    )
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Filter to only included attributes if specified
    if inputs["included_attributes"]:
        filtered_data = []
        for country in data:
            filtered_country = {}
            for attr in inputs["included_attributes"]:
                if attr in country:
                    filtered_country[attr] = country[attr]
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data