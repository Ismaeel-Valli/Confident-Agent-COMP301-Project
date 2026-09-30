import requests

def solve(inputs):
    """
    Look up countries by exact match on their subregion using REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - value: The subregion to match exactly
            - results_to_skip: Number of results to skip (pagination)
            - excluded_attributes: List of country attributes to exclude from response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response. None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    subregion = inputs["value"]
    skip = inputs["results_to_skip"]
    excluded_attrs = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    url = f"{base_url}/v5/countries?subregion={subregion}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Filter out excluded attributes from each country object
    if excluded_attrs:
        filtered_data = []
        for country in data:
            filtered_country = {}
            for key, value in country.items():
                if key not in excluded_attrs:
                    filtered_country[key] = value
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data