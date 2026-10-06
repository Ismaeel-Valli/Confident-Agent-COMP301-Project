import requests

def solve(inputs):
    """
    Search REST Countries v5 API for country codes.
    
    Args:
        inputs (dict): Dictionary containing:
            - results_to_skip (int): Number of results to skip (offset)
            - excluded_attributes (list): Attributes to exclude from response
            - search_text (str): Search term for country names
            - credential (str): API key/credential
    
    Returns:
        dict or None: Decoded JSON response, or None if empty but successful
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build query parameters
    params = {
        "search": inputs["search_text"],
        "skip": inputs["results_to_skip"]
    }
    
    # Make the API request to the correct endpoint
    response = requests.get(
        f"{base_url}/v3.1/search",
        params=params,
        headers={"Authorization": f"Bearer {inputs['credential']}"}
    )
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    # Filter out excluded attributes if any
    if inputs["excluded_attributes"]:
        filtered_data = []
        for country in data:
            filtered_country = {k: v for k, v in country.items() 
                              if k not in inputs["excluded_attributes"]}
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data