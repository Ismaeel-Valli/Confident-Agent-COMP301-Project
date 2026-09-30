import requests

def solve(inputs):
    """
    Look up countries by exact match on common country name using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The exact country name to match
            - results_to_skip: Number of results to skip (for pagination)
            - excluded_attributes: List of attributes to exclude from response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build query parameters
    params = {
        "name": inputs["value"],
        "skip": inputs["results_to_skip"]
    }
    
    # Make the request with credential in header
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(
        base_url + "/v5.1",
        params=params,
        headers=headers
    )
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If no results, return None as per spec for successful empty response
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