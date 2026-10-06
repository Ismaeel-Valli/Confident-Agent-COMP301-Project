import requests

def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Three-letter ISO country code to match exactly
            - results_to_skip: Number of results to skip
            - excluded_attributes: List of attributes to exclude from response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com/v3.1/country"
    
    # Build the query parameters
    params = {
        "code": inputs["value"],
        "skip": inputs["results_to_skip"]
    }
    
    # Make the API request with credentials in headers
    response = requests.get(
        base_url,
        params=params,
        headers={"Authorization": f"Bearer {inputs['credential']}"}
    )
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    # Exclude specified attributes from each country object
    if inputs["excluded_attributes"]:
        for attr in inputs["excluded_attributes"]:
            if attr in data:
                del data[attr]
    
    return data