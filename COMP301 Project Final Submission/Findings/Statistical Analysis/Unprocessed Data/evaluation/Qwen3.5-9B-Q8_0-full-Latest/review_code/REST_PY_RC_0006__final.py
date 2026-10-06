import requests

def solve(inputs):
    """
    Search country names in REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return
            - search_text (str): Search term for country names
            - credential (str): Caller-supplied authentication token
    
    Returns:
        list or None: Decoded JSON response as a list, or None if successful but empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    search_text = inputs["search_text"]
    result_limit = inputs["result_limit"]
    credential = inputs["credential"]
    
    # Construct the URL with query parameters
    url = f"{base_url}/v5/search?name={search_text}&limit={result_limit}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses
        response.raise_for_status()
        
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