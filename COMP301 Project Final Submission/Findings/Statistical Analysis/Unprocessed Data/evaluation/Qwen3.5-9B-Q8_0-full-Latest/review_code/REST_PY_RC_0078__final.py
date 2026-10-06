import requests

def solve(inputs):
    """
    Look up countries by exact match on their common country name using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The exact country name to match
            - result_limit: Maximum number of results to return
            - excluded_attributes: List of attributes to exclude from the response
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build the query parameters
    params = {
        "name": inputs["value"],
        "limit": inputs["result_limit"]
    }
    
    # Make the GET request with credentials in headers
    response = requests.get(
        f"{base_url}/v5.0/countries",
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
        for country in data:
            for attr in inputs["excluded_attributes"]:
                if attr in country:
                    del country[attr]
    
    return data