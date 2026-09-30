import requests

def solve(inputs):
    """
    Look up countries by exact match on their common country name using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The exact country name to match
            - result_limit: Maximum number of results to return
            - results_to_skip: Number of results to skip
            - credential: Caller-supplied authentication credential
    
    Returns:
        list or None: Decoded JSON response (list of countries) or None for empty successful response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    # Construct the URL with query parameters for exact match, limit, and skip
    url = f"{base_url}/v5.0/countries?name={value}&limit={result_limit}&skip={results_to_skip}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # Return None for successful empty response (status 200 with no data)
        if not data:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")