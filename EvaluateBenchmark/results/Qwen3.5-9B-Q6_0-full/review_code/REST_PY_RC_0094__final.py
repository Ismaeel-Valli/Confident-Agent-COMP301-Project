import requests

def solve(inputs):
    """
    Look up countries by exact region match from REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - value: Region to match exactly
            - result_limit: Maximum number of results
            - results_to_skip: Number of results to skip
            - excluded_attributes: List of attributes to exclude from response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    region = inputs["value"]
    limit = inputs["result_limit"]
    skip = inputs["results_to_skip"]
    excluded_attrs = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "region": region,
        "limit": limit,
        "skip": skip
    }
    
    # Make the API request with credentials in header
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(f"{base_url}/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
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