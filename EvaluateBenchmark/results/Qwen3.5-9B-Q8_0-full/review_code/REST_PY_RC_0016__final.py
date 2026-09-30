import requests

def solve(inputs):
    """
    Look up countries by exact match on their two-letter ISO country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Two-letter ISO country code to match exactly
            - included_attributes (list): List of attributes to return
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    country_code = inputs["value"]
    credential = inputs["credential"]
    included_attributes = inputs.get("included_attributes", [])
    
    # Build query parameters
    params = {
        "code": country_code,
        "format": "json",
        "fields": ",".join(included_attributes) if included_attributes else None
    }
    
    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    try:
        response = requests.get(f"{base_url}/v5.0/country", params=params, headers=headers)
        
        # Raise exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Decode JSON response
        data = response.json()
        
        # Return None for successful empty response (no countries found)
        if not data:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")
    except ValueError as e:
        raise Exception(f"Failed to decode JSON response: {e}")