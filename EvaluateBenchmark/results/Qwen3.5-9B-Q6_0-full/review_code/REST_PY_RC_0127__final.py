import requests

def solve(inputs):
    """
    Look up countries by exact currency code match from REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - value: Currency code to match exactly
            - results_to_skip: Number of results to skip
            - included_attributes: List of attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com/v5"
    currency_code = inputs["value"]
    skip = inputs["results_to_skip"]
    attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters for exact match on currency code
    params = {
        "currency": currency_code,
        "skip": skip
    }
    
    # Make the API request with credentials in headers
    response = requests.get(
        base_url,
        params=params,
        headers={"Authorization": f"Bearer {credential}"}
    )
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    data = response.json()
    
    # Filter to only include requested attributes
    if isinstance(data, list):
        filtered_data = []
        for country in data:
            filtered_country = {}
            for attr in attributes:
                if attr in country:
                    filtered_country[attr] = country[attr]
            filtered_data.append(filtered_country)
        return filtered_data
    
    elif isinstance(data, dict):
        filtered_country = {}
        for attr in attributes:
            if attr in data:
                filtered_country[attr] = data[attr]
        return filtered_country
    
    else:
        # If response is not a list or dict, return as-is
        return data