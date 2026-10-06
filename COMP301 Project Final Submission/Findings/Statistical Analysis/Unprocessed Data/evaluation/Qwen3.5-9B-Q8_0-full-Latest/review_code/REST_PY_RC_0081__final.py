import requests

def solve(inputs):
    """
    Look up countries by exact match on common name using REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - value: Country name to match exactly
            - result_limit: Maximum number of results
            - results_to_skip: Number of results to skip
            - included_attributes: List of attributes to include in response
            - credential: Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response (list of countries) or None for empty successful response
        Raises: Exception for unsuccessful HTTP response
    """
    base_url = "https://api.restcountries.com/v3.1/countries"
    
    # Build query parameters
    params = {
        "name": inputs["value"],
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"]
    }
    
    # Make the request with provided credential
    response = requests.get(
        base_url,
        params=params,
        headers={"Authorization": f"Bearer {inputs['credential']}"}
    )
    
    # Raise exception for unsuccessful HTTP response
    response.raise_for_status()
    
    # Decode JSON response
    data = response.json()
    
    # Return None for successful empty response (empty list)
    if len(data) == 0:
        return None
    
    # Filter to only included attributes
    if inputs["included_attributes"]:
        filtered_data = []
        for country in data:
            filtered_country = {}
            for attr in inputs["included_attributes"]:
                if attr in country:
                    filtered_country[attr] = country[attr]
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data