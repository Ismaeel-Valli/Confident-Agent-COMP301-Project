import requests

def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Currency code to match exactly
            - result_limit: Maximum number of results
            - included_attributes: List of country attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response, or None if empty but successful
    """
    base_url = "https://api.restcountries.com/v3.1/countries"
    
    # Build the query parameters
    params = {
        "currency": inputs["value"],
        "limit": inputs["result_limit"]
    }
    
    # Make the request with the provided credential
    response = requests.get(
        base_url,
        params=params
    )
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # If the response is empty but successful, return None
    if not data:
        return None
    
    # Filter to only include the requested attributes
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