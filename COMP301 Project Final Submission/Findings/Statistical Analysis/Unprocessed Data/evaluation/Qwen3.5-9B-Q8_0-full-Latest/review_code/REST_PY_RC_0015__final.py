import requests
import json

def solve(inputs):
    """
    Search REST Countries v5 by text and return filtered attributes.
    
    Args:
        inputs (dict): Must contain:
            - included_attributes (list): Attributes to include in response
            - search_text (str): Search term for country names
            - credential (str): API key/credential
    
    Returns:
        dict or None: Decoded JSON response, or None if empty but successful
        Raises: Exception on unsuccessful HTTP response
    """
    api_key = inputs["credential"]
    search_text = inputs["search_text"]
    included_attributes = inputs["included_attributes"]
    
    # REST Countries v5 uses /v3.1/countries endpoint with query params
    url = "https://api.restcountries.com/v3.1/countries"
    
    params = {
        "name": search_text,
        "fields": ",".join(included_attributes) if included_attributes else None
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # Return None for successful empty response
        if not data:
            return None
        
        return data
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")