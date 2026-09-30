import requests

def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Three-letter ISO country code to match exactly
            - included_attributes (list): Attributes to return in the response
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    country_code = inputs["value"]
    credential = inputs["credential"]
    
    # Construct the API endpoint for exact match by three-letter ISO code
    url = f"{base_url}/v3.0/country/{country_code}"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # If the country is not found, the API returns an empty object or similar
        # We return None for successful empty responses
        if not data:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")