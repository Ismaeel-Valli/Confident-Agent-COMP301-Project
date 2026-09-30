def solve(inputs):
    """
    Look up countries by exact match on their two-letter ISO country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The two-letter ISO country code to match exactly
            - result_limit: Maximum number of results to return
            - excluded_attributes: List of country attributes to exclude from results
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    import requests
    
    # Extract inputs
    iso_code = inputs["value"]
    result_limit = inputs["result_limit"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    credential = inputs["credential"]
    
    # Build the API URL for REST Countries v5
    # Using /v3.1/countries/{code} endpoint for exact match by ISO code
    base_url = "https://api.restcountries.com"
    url = f"{base_url}/v3.1/countries/{iso_code}"
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {credential}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for unsuccessful HTTP responses
        
        data = response.json()
        
        # Check if the response is an empty list (no countries found)
        if isinstance(data, list) and len(data) == 0:
            return None
        
        # Filter out excluded attributes from each country object
        filtered_countries = []
        for country in data:
            filtered_country = {}
            for key, value in country.items():
                if key not in excluded_attributes:
                    filtered_country[key] = value
            filtered_countries.append(filtered_country)
        
        # Apply result limit
        return filtered_countries[:result_limit]
        
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")
    except (KeyError, TypeError) as e:
        raise Exception(f"Invalid input data: {e}")