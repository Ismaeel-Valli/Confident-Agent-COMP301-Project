import requests

def solve(inputs):
    """
    Retrieves one page of countries from REST Countries v5 API using provided credentials.
    
    Args:
        inputs (dict): A dictionary containing 'credential' key with necessary permissions.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
        
    Raises:
        requests.exceptions.RequestException: If HTTP response is unsuccessful.
    """
    # Base URL for REST Countries v5 API (assuming standard public endpoint)
    base_url = "https://restcountries.com/v3.1/all"
    
    # Prepare headers with provided credential if needed
    headers = {}
    if inputs.get("credential"):
        # Assuming credential might be a Bearer token or similar
        headers["Authorization"] = f"Bearer {inputs['credential']}"
    
    try:
        response = requests.get(base_url, headers=headers)
        
        # Raise exception for unsuccessful HTTP responses (4xx, 5xx)
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