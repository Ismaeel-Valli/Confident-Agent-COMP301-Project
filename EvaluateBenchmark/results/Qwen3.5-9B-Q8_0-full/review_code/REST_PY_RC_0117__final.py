import requests

def solve(inputs):
    """
    Look up countries by exact match on their bordering country code using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Country code to match exactly in borders
            - result_limit: Maximum number of results
            - results_to_skip: Number of results to skip
            - included_attributes: List of attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    """
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # REST Countries v5 API endpoint for searching by bordering country code
    base_url = "https://api.restcountries.com/v5.0"
    url = f"{base_url}/search/borders/{value}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    params = {
        "limit": result_limit,
        "skip": results_to_skip,
        "fields": ",".join(included_attributes) if included_attributes else None
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Return None for successful empty response (empty list)
        if isinstance(data, list) and len(data) == 0:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")