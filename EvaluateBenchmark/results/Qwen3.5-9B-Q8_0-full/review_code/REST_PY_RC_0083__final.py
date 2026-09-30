import requests

def solve(inputs):
    """
    Look up countries by exact match on their region using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - "value": The region value to match exactly
            - "credential": Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    api_url = "https://api.restcountries.com/v5/countries"
    
    # Build query parameters for exact region match
    params = {
        "region": inputs["value"]
    }
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    try:
        response = requests.get(api_url, params=params, headers=headers)
        
        # Raise exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Decode JSON response
        data = response.json()
        
        # Return None for successful empty response
        if not data:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")
    except ValueError as e:
        raise Exception(f"Failed to decode JSON response: {e}")