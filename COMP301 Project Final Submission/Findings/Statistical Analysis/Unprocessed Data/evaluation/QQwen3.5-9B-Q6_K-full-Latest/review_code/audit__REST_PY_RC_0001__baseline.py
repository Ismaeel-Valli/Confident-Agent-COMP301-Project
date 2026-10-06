import requests

def solve(inputs):
    """
    Retrieves one page of countries from REST Countries v5 API using provided credentials.
    
    Args:
        inputs (dict): A dictionary containing 'credential' key with necessary permissions.
        
    Returns:
        dict or None: The decoded JSON response, or None if the response is successfully empty.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    # Base URL for REST Countries v5 API
    base_url = "https://restcountries.com/v5.1"
    
    # Endpoint to retrieve countries (example endpoint; adjust if specific one is needed)
    endpoint = "/countries"
    
    # Construct the full URL
    url = f"{base_url}{endpoint}"
    
    # Prepare headers with credentials
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
        response.raise_for_status()
        
        # Decode the JSON response
        data = response.json()
        
        # Return None if the response is successfully empty
        if not data:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Unsuccessful HTTP response: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")