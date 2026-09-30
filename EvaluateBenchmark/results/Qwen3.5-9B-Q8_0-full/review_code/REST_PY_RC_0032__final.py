import requests

def solve(inputs):
    """
    Look up countries by exact match on their two-letter ISO country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The two-letter ISO country code to match exactly
            - result_limit: Maximum number of results to return
            - excluded_attributes: List of country attributes to exclude from results
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        list or None: Decoded JSON response (list of countries) or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build the query parameters
    params = {
        "code": inputs["value"],
        "limit": inputs["result_limit"]
    }
    
    # Make the API request with the provided credential
    response = requests.get(
        f"{base_url}/v5.0/countries",
        params=params,
        headers={"Authorization": f"Bearer {inputs['credential']}"}
    )
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # Filter out excluded attributes if any are specified
    if inputs["excluded_attributes"]:
        filtered_data = []
        for country in data:
            filtered_country = {k: v for k, v in country.items() 
                              if k not in inputs["excluded_attributes"]}
            filtered_data.append(filtered_country)
        return filtered_data
    
    # Return the decoded JSON response
    # Return None for a successful empty response
    return data if data else None