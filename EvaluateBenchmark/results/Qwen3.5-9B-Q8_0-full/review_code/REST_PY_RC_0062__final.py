import requests

def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Three-letter ISO country code to match exactly
            - result_limit: Maximum number of results to return
            - included_attributes: List of attributes to include in the response
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Base URL for REST Countries v5 API
    base_url = "https://api.restcountries.com/v5"
    
    # Construct the endpoint for exact match lookup by ISO 3-letter code
    url = f"{base_url}/country/{value}"
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Raise exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Decode JSON response
        data = response.json()
        
        # If the response is an empty list (no countries found), return None
        if isinstance(data, list) and len(data) == 0:
            return None
        
        # Filter attributes if specified
        if included_attributes:
            filtered_data = []
            for country in data:
                filtered_country = {}
                for attr in included_attributes:
                    if attr in country:
                        filtered_country[attr] = country[attr]
                filtered_data.append(filtered_country)
            return filtered_data
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")