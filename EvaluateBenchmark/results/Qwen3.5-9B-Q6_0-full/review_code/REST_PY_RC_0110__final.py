import requests

def solve(inputs):
    """
    Look up countries by exact match on their bordering country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Country code to match exactly
            - included_attributes: List of attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    value = inputs["value"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build the API URL
    base_url = "https://api.restcountries.com/v5.0"
    url = f"{base_url}/countries"
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {credential}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # If the response is empty (no borders found), return None
        if not data:
            return None
        
        # Filter attributes if specified
        if included_attributes:
            filtered_data = {}
            for key, val in data.items():
                if key in included_attributes:
                    filtered_data[key] = val
            return filtered_data
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")