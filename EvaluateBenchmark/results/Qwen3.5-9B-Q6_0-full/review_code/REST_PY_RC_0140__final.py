import requests

def solve(inputs):
    """
    Look up countries by exact match on their calling code from REST Countries v5.
    
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
    
    # Build query parameters
    params = {
        "callingCode": inputs["value"],
        "skip": inputs["results_to_skip"]
    }
    
    # Make the API request with provided credential
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(f"{base_url}/v5/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # If no results, return None for successful empty response
    if not data or (isinstance(data, list) and len(data) == 0):
        return None
    
    # Filter out excluded attributes from each country object
    if inputs["excluded_attributes"]:
        filtered_data = []
        for country in data:
            filtered_country = {k: v for k, v in country.items() 
                             if k not in inputs["excluded_attributes"]}
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data