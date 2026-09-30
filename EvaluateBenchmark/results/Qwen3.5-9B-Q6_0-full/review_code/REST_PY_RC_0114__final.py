import requests

def solve(inputs):
    """
    Look up countries by exact match on their bordering country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Country code to match exactly
            - result_limit: Maximum number of results
            - excluded_attributes: List of attributes to exclude from response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    excluded_attributes = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # REST Countries v5 API endpoint for bordering countries
    base_url = "https://api.restcountries.com/v5.0"
    url = f"{base_url}/borders/{value}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # Filter out excluded attributes if any
        if excluded_attributes:
            filtered_data = {}
            for key in data.keys():
                if key not in excluded_attributes:
                    filtered_data[key] = data[key]
            return filtered_data
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")