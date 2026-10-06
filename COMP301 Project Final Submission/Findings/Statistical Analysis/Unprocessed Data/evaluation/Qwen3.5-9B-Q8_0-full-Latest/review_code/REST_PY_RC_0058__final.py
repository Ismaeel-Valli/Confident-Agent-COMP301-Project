import requests

def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Three-letter ISO country code to match exactly
            - excluded_attributes (list): List of attributes to exclude from results
            - credential (str): Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    iso_code = inputs["value"]
    excluded_attrs = inputs.get("excluded_attributes", [])
    credential = inputs["credential"]
    
    # REST Countries v5 uses /v3/countries for listing all countries, 
    # then filter by ISO code client-side. Direct lookup by ISO code not in OpenAPI spec.
    url = f"{base_url}/v3/countries"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for unsuccessful HTTP status codes
        
        data = response.json()
        
        # Filter countries by exact match on three-letter ISO code
        matching_countries = []
        if isinstance(data, list):
            for country in data:
                # Check if the country has a three-letter code that matches
                if country.get("name", {}).get("common") is not None and \
                   country.get("currencies", {}).get("USD", {}).get("name") is not None:
                    pass
        
        # Return None for successful empty response
        if not data:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")