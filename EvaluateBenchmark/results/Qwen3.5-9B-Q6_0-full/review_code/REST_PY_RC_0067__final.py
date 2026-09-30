import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Parameters:
        inputs (dict): Dictionary containing:
            - results_to_skip (int): Number of results to skip (offset)
            - excluded_attributes (list): Attributes to exclude from response
            - search_text (str): Search term for filtering
            - credential (str): API credential/token
    
    Returns:
        dict or None: Decoded JSON response, or None if empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com/v5/countries"
    
    # Build query parameters
    params = {
        "skip": inputs["results_to_skip"],
        "search": inputs.get("search_text", ""),
        "credential": inputs["credential"]
    }
    
    # Make the request
    response = requests.get(base_url, params=params)
    
    # Check for successful HTTP response
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    # Decode JSON response
    data = response.json()
    
    # Handle empty response
    if not data:
        return None
    
    # Exclude specified attributes from each country object
    excluded_attrs = inputs.get("excluded_attributes", [])
    filtered_data = []
    
    for country in data:
        filtered_country = {k: v for k, v in country.items() 
                          if k not in excluded_attrs}
        filtered_data.append(filtered_country)
    
    return filtered_data