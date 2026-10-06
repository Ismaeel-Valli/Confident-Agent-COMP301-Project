import requests

def solve(inputs):
    """
    Search REST Countries v5 by country codes using provided credentials.
    
    Args:
        inputs (dict): Contains:
            - result_limit (int): Maximum number of results to return
            - included_attributes (list): Attributes to include in response
            - search_text (str): Search term for country names/codes
            - credential (str): API key/credential
    
    Returns:
        dict or None: Decoded JSON response, or None if empty successful response
    """
    base_url = "https://api.restcountries.com"
    
    # Build query parameters
    params = {
        'limit': inputs['result_limit'],
        'search': inputs['search_text']
    }
    
    # Add credential to headers
    headers = {
        'X-API-Key': inputs['credential']
    }
    
    try:
        response = requests.get(
            f"{base_url}/v5.0/countries",
            params=params,
            headers=headers
        )
        
        # Raise exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        data = response.json()
        
        # If successful but empty, return None
        if not data:
            return None
        
        # Filter to only included attributes if specified
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
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")