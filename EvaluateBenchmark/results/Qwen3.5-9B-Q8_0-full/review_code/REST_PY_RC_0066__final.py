import requests

def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Three-letter ISO country code to match exactly
            - results_to_skip (int): Number of results to skip
            - included_attributes (list): List of attributes to return
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build the query URL with exact match on alpha-3 code
    url = f"{base_url}/v5.0/countries?alpha-3={inputs['value']}"
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    # Make the GET request
    response = requests.get(url, headers=headers)
    
    # Raise exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode JSON response
    data = response.json()
    
    # Handle empty response
    if not data:
        return None
    
    # Filter to only included attributes if specified
    if inputs['included_attributes']:
        filtered_results = []
        for country in data:
            filtered_country = {}
            for attr in inputs['included_attributes']:
                if attr in country:
                    filtered_country[attr] = country[attr]
            filtered_results.append(filtered_country)
        return filtered_results
    
    return data