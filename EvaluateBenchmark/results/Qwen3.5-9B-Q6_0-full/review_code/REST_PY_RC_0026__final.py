import requests

def solve(inputs):
    """
    Search country names using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return
            - included_attributes (list): List of attributes to include in response
            - search_text (str): Search term for country names
            - credential (str): Caller-supplied API credential
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com/v5.0"
    
    # Build query parameters
    params = {
        'search': inputs['search_text'],
        'limit': inputs['result_limit']
    }
    
    # Make the API request with credential in header
    headers = {
        'Authorization': f'Bearer {inputs["credential"]}'
    }
    
    response = requests.get(f"{base_url}/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If successful but empty response, return None
    if not data:
        return None
    
    # Filter to only include requested attributes
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