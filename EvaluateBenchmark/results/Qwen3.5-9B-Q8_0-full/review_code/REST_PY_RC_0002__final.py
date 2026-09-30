import requests

def solve(inputs):
    """
    Search country names in REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - search_text (str): Search term for country names
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    search_text = inputs["search_text"]
    credential = inputs["credential"]
    
    # Construct the API endpoint for searching countries by name
    url = f"{base_url}/v5/search?name={search_text}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # Return None for successful empty response
        if not data:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")