import requests

def solve(inputs):
    """
    Look up countries by exact match on their subregion using REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - value: The subregion to match exactly
            - result_limit: Maximum number of results
            - excluded_attributes: List of country attributes to exclude from response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    subregion = inputs["value"]
    limit = inputs["result_limit"]
    excluded_attrs = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "subregion": subregion,
        "limit": limit
    }
    
    # Make the API request with credentials in headers
    response = requests.get(
        f"{base_url}/v5/countries",
        params=params,
        headers={"Authorization": f"Bearer {credential}"}
    )
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    data = response.json()
    
    # Filter out excluded attributes from each country object
    if excluded_attrs:
        filtered_data = []
        for country in data:
            filtered_country = {k: v for k, v in country.items() if k not in excluded_attrs}
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data