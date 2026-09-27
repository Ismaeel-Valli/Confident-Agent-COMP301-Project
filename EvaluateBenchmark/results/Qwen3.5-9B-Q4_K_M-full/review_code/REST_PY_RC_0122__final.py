import requests

def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - 'value': The currency code to match exactly (e.g., 'USD')
            - 'included_attributes': List of country attributes to return
            - 'credential': Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com/v5.0"
    
    # Build the query URL with currency code parameter
    url = f"{base_url}/currency/{inputs['value']}"
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Raise exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Decode JSON response
        data = response.json()
        
        # If response is empty (no countries found), return None
        if not data:
            return None
        
        # Filter to only include requested attributes
        if inputs['included_attributes']:
            filtered_data = []
            for country in data:
                filtered_country = {}
                for attr in inputs['included_attributes']:
                    if attr in country:
                        filtered_country[attr] = country[attr]
                filtered_data.append(filtered_country)
            return filtered_data
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")