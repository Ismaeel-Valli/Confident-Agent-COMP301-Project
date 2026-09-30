import requests

def solve(inputs):
    """
    Look up countries by exact match on their capital city using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The capital city to match exactly
            - result_limit: Maximum number of results to return
            - excluded_attributes: List of country attributes to exclude from response
            - credential: Caller-supplied authentication credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    # Base URL for REST Countries v5 API
    base_url = "https://api.restcountries.com/v5"
    
    # Build the query parameters
    params = {
        "capital": inputs["value"],
        "limit": inputs["result_limit"]
    }
    
    # Make the API request with the provided credential
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(
        base_url,
        params=params,
        headers=headers
    )
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    # Filter out excluded attributes from each country object
    if inputs["excluded_attributes"]:
        filtered_data = []
        for country in data:
            filtered_country = {
                key: value 
                for key, value in country.items() 
                if key not in inputs["excluded_attributes"]
            }
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data