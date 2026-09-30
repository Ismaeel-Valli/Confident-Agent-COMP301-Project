import requests

def solve(inputs):
    """
    Look up countries by exact match on their calling code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The calling code to match exactly
            - result_limit: Maximum number of results to return
            - excluded_attributes: List of country attributes to exclude from response
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    calling_code = inputs["value"]
    result_limit = inputs["result_limit"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    credential = inputs["credential"]
    
    # Build the URL with query parameters
    params = {
        "fields": ",".join(excluded_attributes) if excluded_attributes else "",
        "limit": result_limit,
        "callingcode": calling_code
    }
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    url = f"{base_url}/v5/country?callingcode={calling_code}&fields={','.join(excluded_attributes) if excluded_attributes else ''}&limit={result_limit}"
    
    try:
        response = requests.get(url, headers=headers, params=params)
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