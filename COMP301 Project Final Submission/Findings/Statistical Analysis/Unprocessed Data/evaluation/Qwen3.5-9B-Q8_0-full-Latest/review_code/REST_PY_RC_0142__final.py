import requests

def solve(inputs):
    """
    Look up countries by exact match on their calling code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The calling code to match exactly
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip
            - excluded_attributes: List of country attributes to exclude from response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build the query parameters
    params = {
        "callingcode": inputs["value"],
        "limit": str(inputs["result_limit"]),
        "skip": str(inputs["results_to_skip"])
    }
    
    # Make the API request
    response = requests.get(
        f"{base_url}/v5.0/countries",
        params=params,
        headers={"Authorization": inputs["credential"]}
    )
    
    # Check for unsuccessful HTTP response
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for successful empty response
    if not data:
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