import requests

def solve(inputs):
    """
    Retrieves one page of countries from REST Countries v5 using provided credentials.
    
    Args:
        inputs (dict): A dictionary containing 'credential' key with necessary permissions.
        
    Returns:
        dict or None: Decoded JSON response, or None if the response is successfully empty.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    # Base URL for REST Countries v5 API
    base_url = "https://restcountries.com/v5.1"
    
    # Construct the endpoint to get one page of countries (typically /data)
    endpoint = "/data"
    
    # Prepare the request with the provided credential
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    try:
        response = requests.get(f"{base_url}{endpoint}", headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses (4xx, 5xx)
        response.raise_for_status()
        
        # Decode the JSON response
        data = response.json()
        
        # Return None if the response is successfully empty
        if not data:
            return None
            
        return data
        
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP request failed: {e}") from e
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}") from e