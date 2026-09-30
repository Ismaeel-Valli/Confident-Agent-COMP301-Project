import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - search_text (str): Search term for filtering countries
            - credential (str): Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty response
        Raises: Exception for unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build the request URL with search parameter
    url = f"{base_url}/v5/countries?search={inputs['search_text']}"
    
    # Prepare headers with credential
    headers = {
        "Authorization": inputs["credential"],
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for unsuccessful HTTP responses
        
        data = response.json()
        
        # Return None if successful but empty response
        if not data:
            return None
            
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")