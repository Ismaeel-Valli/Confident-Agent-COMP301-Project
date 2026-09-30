import requests

def solve(inputs):
    """
    Search REST Countries v5 using caller-supplied credential.
    
    inputs:
        - results_to_skip (int): Number of results to skip (offset)
        - excluded_attributes (list[str]): Attributes to exclude from response
        - search_text (str): Search term for country names
        - credential (str): API key/credential
    
    Returns:
        - Decoded JSON response, or None if successful but empty
        - Raises exception on unsuccessful HTTP response
    """
    base_url = "https://api.restcountries.com"
    
    # Build query parameters
    params = {
        "search": inputs["search_text"],
        "skip": inputs["results_to_skip"]
    }
    
    # Make the request with the provided credential
    response = requests.get(
        f"{base_url}/v5/countries",
        params=params,
        headers={"Authorization": f"Bearer {inputs['credential']}"}
    )
    
    # Raise exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode JSON response
    data = response.json()
    
    # Return None if successful but empty
    if not data:
        return None
    
    # Exclude specified attributes from each country object
    excluded = set(inputs["excluded_attributes"])
    filtered_data = []
    for country in data:
        filtered_country = {k: v for k, v in country.items() if k not in excluded}
        filtered_data.append(filtered_country)
    
    return filtered_data