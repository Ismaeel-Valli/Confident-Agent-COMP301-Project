import requests

def solve(inputs):
    """
    Look up countries by exact match on their calling code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The calling code to match exactly
            - results_to_skip: Number of results to skip
            - excluded_attributes: List of country attributes to exclude
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    calling_code = inputs["value"]
    skip = inputs["results_to_skip"]
    excluded_attrs = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "callingcode": calling_code,
        "skip": skip
    }
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(
        base_url + "/v5.0/countries",
        params=params,
        headers=headers
    )
    
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