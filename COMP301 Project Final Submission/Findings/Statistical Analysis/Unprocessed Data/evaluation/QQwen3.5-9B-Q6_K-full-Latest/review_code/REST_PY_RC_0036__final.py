import requests


def solve(inputs):
    """
    Look up countries by exact ISO code using REST Countries v5 API.
    
    inputs:
        - value: Two-letter ISO country code to match exactly
        - results_to_skip: Number of results to skip (for pagination)
        - included_attributes: List of attributes to include in response
        - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        - Decoded JSON response, or None for successful empty response
        - Raises exception for unsuccessful HTTP response
    """
    base_url = "https://api.restcountries.com"
    iso_code = inputs["value"]
    skip = inputs["results_to_skip"]
    attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    url = f"{base_url}/v5.0/country/{iso_code}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If no countries found (empty list), return None for successful empty response
    if isinstance(data, list) and len(data) == 0:
        return None
    
    # Filter to only include requested attributes
    if isinstance(data, list):
        filtered_results = []
        for country in data:
            filtered_country = {}
            for attr in attributes:
                if attr in country:
                    filtered_country[attr] = country[attr]
            filtered_results.append(filtered_country)
        return filtered_results
    
    # If single object response, filter attributes
    elif isinstance(data, dict):
        filtered_country = {}
        for attr in attributes:
            if attr in data:
                filtered_country[attr] = data[attr]
        return filtered_country
    
    return data