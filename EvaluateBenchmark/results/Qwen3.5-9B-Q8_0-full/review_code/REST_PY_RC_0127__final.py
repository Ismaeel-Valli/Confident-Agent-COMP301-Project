import requests

def solve(inputs):
    """
    Look up countries by exact currency code match from REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - value: Currency code to match exactly
            - results_to_skip: Number of results to skip
            - included_attributes: List of attributes to return
            - credential: API key for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if empty successful response
    """
    base_url = "https://api.restcountries.com/v5.0"
    
    # Build query parameters
    params = {
        'currency': inputs['value'],
        'skip': inputs['results_to_skip']
    }
    
    # Make the API request with credentials in header
    headers = {
        'x-rcc-api-key': inputs['credential']
    }
    
    response = requests.get(f"{base_url}/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If empty response, return None
    if not data:
        return None
    
    # Filter to only included attributes
    if inputs['included_attributes']:
        filtered_data = []
        for country in data:
            filtered_country = {}
            for attr in inputs['included_attributes']:
                if attr in country:
                    filtered_country[attr] = country[attr]
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data