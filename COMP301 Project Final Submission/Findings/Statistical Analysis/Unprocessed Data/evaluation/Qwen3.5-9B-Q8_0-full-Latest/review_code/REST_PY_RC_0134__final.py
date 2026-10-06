import requests

def solve(inputs):
    """
    Look up countries by exact match on their calling code using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The calling code to match exactly (string)
            - included_attributes: List of attributes to include in response
            - credential: Caller-supplied credential for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty response
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build the request URL with the calling code parameter
    url = f"{base_url}/v5/calling-code/{inputs['value']}"
    
    # Prepare headers with the credential
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses (4xx, 5xx)
        response.raise_for_status()
        
        # Decode the JSON response
        data = response.json()
        
        # Return None if the response is empty but successful
        if not data:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")