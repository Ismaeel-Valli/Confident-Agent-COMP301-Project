import requests

def solve(inputs):
    """
    Look up countries by exact match on their two-letter ISO country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Two-letter ISO country code to match exactly
            - result_limit (int): Maximum number of results
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    iso_code = inputs["value"]
    limit = inputs["result_limit"]
    credential = inputs["credential"]
    
    # REST Countries v5 endpoint for searching by ISO code
    base_url = "https://api.restcountries.com"
    url = f"{base_url}/v5/search?iso={iso_code}&limit={limit}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # Return None for successful empty response (status 200 with no results)
        if not data or len(data) == 0:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")