import requests

def solve(inputs):
    """
    Look up countries by exact match on their common country name using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The exact country name to search for
            - included_attributes: List of attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None if empty successful response
    """
    base_url = "https://api.restcountries.com"
    
    # Build the query URL with exact match on common name
    url = f"{base_url}/v5.1/country?name={inputs['value']}"
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # If no countries found (empty list), return None for successful empty response
        if isinstance(data, list) and len(data) == 0:
            return None
        
        # Filter to only include requested attributes if specified
        if inputs.get('included_attributes'):
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