import requests

def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Three-letter ISO country code to match exactly
            - result_limit (int): Maximum number of results
            - excluded_attributes (list): List of country attributes to exclude
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # REST Countries v5 uses /v5.0/countries endpoint
    url = f"{base_url}/v5.0/countries"
    
    # Prepare headers with credential
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
        
        # Return None for successful empty response
        if not data:
            return None
        
        # Filter by alpha-3 code and exclude specified attributes
        filtered_countries = []
        for country in data:
            if country.get("alpha-3") == inputs["value"]:
                filtered_country = {}
                for key, value in country.items():
                    if key not in inputs["excluded_attributes"]:
                        filtered_country[key] = value
                filtered_countries.append(filtered_country)
        
        return filtered_countries
        
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")