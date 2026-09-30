import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 using the provided credential.
    
    Args:
        inputs (dict): Must contain 'credential' key with the API token.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    credential = inputs["credential"]
    
    # REST Countries v5 base URL - using the correct endpoint for countries list
    base_url = "https://api.restcountries.com/v5"
    
    # Construct the endpoint for one page of countries (list all countries)
    url = f"{base_url}/countries?page=1&limit=10"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Decode the JSON response
        data = response.json()
        
        # Return None for a successful empty response
        if not data:
            return None
            
        return data
        
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")
    except ValueError as e:
        raise Exception(f"Failed to decode JSON response: {e}")