import requests

def solve(inputs):
    """
    Look up countries by exact match on their two-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The two-letter ISO country code to match exactly
            - excluded_attributes: List of country attributes to exclude from results
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    iso_code = inputs["value"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    credential = inputs["credential"]
    
    # Build the API URL with the ISO code parameter
    base_url = "https://api.restcountries.com/v5"
    url = f"{base_url}/country/{iso_code}"
    
    # Prepare headers with the credential
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Decode the JSON response
        data = response.json()
        
        # If the response is empty (successful but no results), return None
        if not data:
            return None
        
        # Filter out excluded attributes from each country object
        filtered_countries = []
        for country in data:
            filtered_country = {}
            for key, value in country.items():
                if key not in excluded_attributes:
                    filtered_country[key] = value
            filtered_countries.append(filtered_country)
        
        return filtered_countries
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")
    except ValueError as e:
        raise Exception(f"Failed to decode JSON response: {e}")