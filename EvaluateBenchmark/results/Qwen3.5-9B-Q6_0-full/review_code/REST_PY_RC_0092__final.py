import requests

def solve(inputs):
    """
    Look up countries by exact match on their region from REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The region to match exactly
            - results_to_skip: Number of results to skip (for pagination)
            - excluded_attributes: List of attributes to exclude from response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com/v5.0/countries"
    
    # Build query parameters
    params = {
        "region": inputs["value"],
        "skip": inputs["results_to_skip"]
    }
    
    # Make the request with credential in headers
    response = requests.get(
        base_url,
        params=params
    )
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # If empty response, return None as per spec
    if not data:
        return None
    
    # Exclude specified attributes from each country object
    if inputs["excluded_attributes"]:
        for country in data:
            for attr in inputs["excluded_attributes"]:
                if attr in country:
                    del country[attr]
    
    return data