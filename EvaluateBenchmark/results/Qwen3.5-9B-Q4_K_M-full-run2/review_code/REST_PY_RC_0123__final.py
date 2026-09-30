def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Currency code to match exactly
            - excluded_attributes (list): List of country attributes to exclude from results
            - credential (str): Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    base_url = "https://api.restcountries.com/v5"
    
    # Build the API endpoint to search by currency code
    url = f"{base_url}/currency/{inputs['value']}"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Raise exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Decode JSON response
        data = response.json()
        
        # If the response is an empty list or empty dict, return None
        if not data:
            return None
        
        # Filter out excluded attributes from each country object
        filtered_countries = []
        for country in data:
            filtered_country = {}
            for key, value in country.items():
                if key not in inputs['excluded_attributes']:
                    filtered_country[key] = value
            filtered_countries.append(filtered_country)
        
        return filtered_countries
        
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")