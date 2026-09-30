import requests

def solve(inputs):
    """
    Look up countries by exact match on their bordering country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Country code to match exactly (bordering country)
            - results_to_skip: Number of results to skip (for pagination)
            - excluded_attributes: List of attributes to exclude from response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    value = inputs["value"]
    results_to_skip = inputs["results_to_skip"]
    excluded_attributes = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Build the query parameters
    params = {
        "border": value,
        "skip": results_to_skip
    }
    
    # Make the request with credentials in header
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(f"{base_url}/v5.0/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If the response is empty (successful but no results), return None
    if not data:
        return None
    
    # Filter out excluded attributes from each country object
    filtered_data = []
    for country in data:
        filtered_country = {key: value for key, value in country.items() 
                          if key not in excluded_attributes}
        filtered_data.append(filtered_country)
    
    return filtered_data