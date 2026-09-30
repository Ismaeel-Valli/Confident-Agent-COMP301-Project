import requests

def solve(inputs):
    """
    Look up countries by exact match on their subregion using REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - value: The subregion to match exactly
            - excluded_attributes: List of country attributes to exclude from results
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    subregion = inputs["value"]
    credential = inputs["credential"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    
    # Build query parameters
    params = {
        "subregion": subregion,
        "format": "json"
    }
    
    # Add credential to headers (assuming Bearer token format)
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(f"{base_url}/v5.0/countries", params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # If the response is an empty list or empty object, return None for successful empty response
        if not data:
            return None
        
        # Filter out countries with excluded attributes
        filtered_countries = []
        for country in data:
            include = True
            for attr in excluded_attributes:
                if attr in country and country[attr]:
                    include = False
                    break
            if include:
                filtered_countries.append(country)
        
        return filtered_countries if filtered_countries else None
        
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")
    except ValueError as e:
        raise Exception(f"JSON decoding failed: {e}")