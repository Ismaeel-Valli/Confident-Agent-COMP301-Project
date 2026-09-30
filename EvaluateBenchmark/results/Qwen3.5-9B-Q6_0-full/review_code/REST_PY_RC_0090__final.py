import requests

def solve(inputs):
    """
    Look up countries by exact match on their region from REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - value: The region to match exactly
            - result_limit: Maximum number of results
            - excluded_attributes: List of country attributes to exclude
            - credential: Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response, or None for empty successful response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    region = inputs["value"]
    limit = inputs["result_limit"]
    excluded_attrs = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    url = f"{base_url}/v5.0/countries?region={region}&limit={limit}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Filter out excluded attributes from each country object
    filtered_data = []
    for country in data:
        filtered_country = {}
        for key, value in country.items():
            if key not in excluded_attrs:
                filtered_country[key] = value
        filtered_data.append(filtered_country)
    
    return filtered_data if filtered_data else None