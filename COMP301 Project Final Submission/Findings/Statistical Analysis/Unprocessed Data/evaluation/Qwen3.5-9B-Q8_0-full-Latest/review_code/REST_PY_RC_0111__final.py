import requests

def solve(inputs):
    """
    Look up countries by exact match on their bordering country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The bordering country code to match exactly
            - excluded_attributes: List of country attributes to exclude from results
            - credential: Caller-supplied credential for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty response
        Raises: Exception for unsuccessful HTTP responses
    """
    # Base URL for REST Countries API v5
    base_url = "https://api.restcountries.com/v5"
    
    # Extract inputs
    value = inputs["value"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    credential = inputs["credential"]
    
    # Build the request URL with the bordering country code parameter
    url = f"{base_url}/borders/{value}"
    
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
        
        # Return None if successful but empty response
        if not data:
            return None
        
        # Filter out excluded attributes from each country object
        filtered_data = []
        for country in data:
            filtered_country = {}
            for key, val in country.items():
                if key not in excluded_attributes:
                    filtered_country[key] = val
            filtered_data.append(filtered_country)
        
        return filtered_data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")
    except ValueError as e:
        raise Exception(f"Failed to decode JSON response: {e}")