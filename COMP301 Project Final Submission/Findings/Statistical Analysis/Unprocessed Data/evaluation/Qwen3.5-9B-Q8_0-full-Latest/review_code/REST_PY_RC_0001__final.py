import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 using the provided credential.
    
    Args:
        inputs (dict): Must contain 'credential' key with the API key/credential string.
        
    Returns:
        dict or None: The decoded JSON response if successful, None for empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    credential = inputs["credential"]
    
    # REST Countries v5 endpoint for listing countries (one page)
    url = "https://api.restcountries.com/v5/countries"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses (4xx, 5xx)
        response.raise_for_status()
        
        # Decode the JSON response
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