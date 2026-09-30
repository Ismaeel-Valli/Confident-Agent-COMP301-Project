import requests


def solve(inputs):
    """
    Look up countries by exact match on their calling code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The calling code to match exactly (string)
            - result_limit: Maximum number of results (int)
            - excluded_attributes: List of country attributes to exclude (list)
            - credential: Caller-supplied credential (str)
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    calling_code = inputs["value"]
    result_limit = inputs["result_limit"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    credential = inputs["credential"]
    
    # Build the query parameters
    params = {
        "callingCode": calling_code,
        "limit": result_limit
    }
    
    # Make the API request with the provided credential
    response = requests.get(
        f"{base_url}/v5/country",
        params=params,
        headers={"Authorization": f"Bearer {credential}"}
    )
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    data = response.json()
    
    # Filter out excluded attributes from each country object
    if excluded_attributes:
        filtered_data = []
        for country in data:
            filtered_country = {k: v for k, v in country.items() 
                             if k not in excluded_attributes}
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data