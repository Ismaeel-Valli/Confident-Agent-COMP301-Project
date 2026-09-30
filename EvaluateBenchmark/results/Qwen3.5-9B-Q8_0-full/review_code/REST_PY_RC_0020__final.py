import requests

def solve(inputs):
    """
    Look up countries by exact match on their two-letter ISO country code.
    
    Args:
        inputs (dict): {
            "value": str,  # Two-letter ISO country code to match exactly
            "excluded_attributes": list[str],  # Attributes to exclude from results
            "credential": str  # Caller-supplied credential with necessary permissions
        }
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    country_code = inputs["value"]
    credential = inputs["credential"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    
    # Construct the API endpoint with exact match query parameter
    url = f"{base_url}/v5.0/countries?code={country_code}"
    
    # Prepare headers with the provided credential
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses (4xx, 5xx)
        response.raise_for_status()
        
        # Decode the JSON response
        data = response.json()
        
        # Return None for successful empty response, otherwise return the data
        if not data:
            return None
        
        # Filter out excluded attributes from each country object
        filtered_countries = []
        for country in data:
            filtered_country = {key: value for key, value in country.items() 
                              if key not in excluded_attributes}
            filtered_countries.append(filtered_country)
        
        return filtered_countries
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")
    except ValueError as e:
        raise Exception(f"Failed to decode JSON response: {e}")