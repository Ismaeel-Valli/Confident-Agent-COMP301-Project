import requests

def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - value: Currency code to match exactly
            - result_limit: Maximum number of results
            - results_to_skip: Number of results to skip
            - excluded_attributes: List of country attributes to exclude
            - credential: Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response (list of countries) or None for empty successful response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    currency_code = inputs["value"]
    limit = inputs["result_limit"]
    skip = inputs["results_to_skip"]
    excluded_attrs = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "currency": currency_code,
        "limit": limit,
        "skip": skip
    }
    
    # Make the request with credentials in headers
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(f"{base_url}/v5/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Filter out excluded attributes from each country object
    if excluded_attrs:
        filtered_data = []
        for country in data:
            filtered_country = {k: v for k, v in country.items() if k not in excluded_attrs}
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data