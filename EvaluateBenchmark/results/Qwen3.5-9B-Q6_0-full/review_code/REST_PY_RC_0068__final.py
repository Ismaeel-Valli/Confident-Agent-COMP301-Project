import requests

def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The three-letter ISO country code to match exactly
            - results_to_skip: Number of results to skip
            - excluded_attributes: List of attributes to exclude from response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    # Extract inputs
    iso_code = inputs["value"]
    skip = inputs["results_to_skip"]
    exclude_attrs = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Build the API URL for REST Countries v5
    # Using /v3.1/countries/{code} endpoint for exact match by ISO 3-letter code
    base_url = "https://api.restcountries.com/v3.1"
    url = f"{base_url}/countries/{iso_code}"
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Raise exception for unsuccessful HTTP responses (4xx, 5xx)
        response.raise_for_status()
        
        # Decode JSON response
        data = response.json()
        
        # If the response is empty (no countries found), return None
        if not data:
            return None
        
        # Filter out excluded attributes from each country object
        if exclude_attrs:
            filtered_data = []
            for country in data:
                filtered_country = {k: v for k, v in country.items() 
                                  if k not in exclude_attrs}
                filtered_data.append(filtered_country)
            return filtered_data
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")
    except ValueError as e:
        raise Exception(f"Failed to decode JSON response: {e}")