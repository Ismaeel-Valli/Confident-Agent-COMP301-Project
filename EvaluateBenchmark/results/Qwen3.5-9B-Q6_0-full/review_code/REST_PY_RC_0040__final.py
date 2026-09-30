import requests

def solve(inputs):
    """
    Look up countries by exact match on their two-letter ISO country code.
    
    Args:
        inputs (dict): Contains:
            - value: The two-letter ISO country code to match exactly
            - results_to_skip: Number of results to skip
            - excluded_attributes: List of attributes to exclude from response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    value = inputs["value"]
    results_to_skip = inputs["results_to_skip"]
    excluded_attributes = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Build the API URL with query parameters for REST Countries v5
    base_url = "https://api.restcountries.com/v5.0"
    url = f"{base_url}/country/{value}"
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for unsuccessful HTTP responses
        
        data = response.json()
        
        # If the response is empty (no country found), return None
        if not data:
            return None
        
        # Filter out excluded attributes from the result
        if excluded_attributes:
            filtered_data = {}
            for key, val in data.items():
                if key not in excluded_attributes:
                    filtered_data[key] = val
            return filtered_data
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")