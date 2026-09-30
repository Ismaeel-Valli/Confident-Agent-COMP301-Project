import requests

def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Three-letter ISO country code to match exactly
            - excluded_attributes (list): List of country attributes to exclude from response
            - credential (str): Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    iso_code = inputs["value"]
    credential = inputs["credential"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    
    # Construct the API endpoint for exact match by ISO 3-letter code
    url = f"{base_url}/v5.0/country/{iso_code}"
    
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
        
        # If the response is empty (no country found), return None
        if not data:
            return None
        
        # Filter out excluded attributes from the response
        filtered_data = {}
        for key, value in data.items():
            if key not in excluded_attributes:
                filtered_data[key] = value
        
        return filtered_data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")
    except ValueError as e:
        raise Exception(f"Failed to decode JSON response: {e}")