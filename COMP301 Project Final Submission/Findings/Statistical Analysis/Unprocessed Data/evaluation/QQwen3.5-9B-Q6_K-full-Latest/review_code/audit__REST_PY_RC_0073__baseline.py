import requests

def solve(inputs):
    """
    Looks up countries by exact match on their common country name using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The exact country name to search for.
            - 'results_to_skip': Number of results to skip (offset).
            - 'credential': API key/credential for authentication.
    
    Returns:
        list or None: Decoded JSON response as a list of countries, or None if the response is empty but successful.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (non-2xx status code).
    """
    base_url = "https://restcountries.com/v3.1"
    endpoint = f"{base_url}/name"
    
    params = {
        'language': 'en',
        'skip': inputs['results_to_skip'],
        'per_page': 1,  # We only need one result for exact match
        'search': inputs['value']
    }
    
    headers = {
        'Authorization': f'Bearer {inputs["credential"]}'
    }
    
    try:
        response = requests.get(endpoint, params=params, headers=headers)
        
        if response.status_code < 200 or response.status_code >= 300:
            raise Exception(f"HTTP error occurred: Status code {response.status_code}")
        
        data = response.json()
        
        # If the search yields no results, return None as per requirements for successful empty response
        if not data:
            return None
        
        return data
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")