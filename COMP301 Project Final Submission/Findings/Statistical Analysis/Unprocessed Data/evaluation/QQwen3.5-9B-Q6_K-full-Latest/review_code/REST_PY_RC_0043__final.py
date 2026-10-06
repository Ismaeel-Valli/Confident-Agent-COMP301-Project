import requests

def solve(inputs):
    """
    Search REST Countries v5 using provided inputs.
    
    Args:
        inputs (dict): Contains:
            - result_limit (int): Maximum number of results
            - results_to_skip (int): Number of results to skip
            - included_attributes (list): Attributes to include in response
            - search_text (str): Search term
            - credential (str): API key/credential
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    """
    base_url = "https://api.restcountries.com"
    
    # Build query parameters
    params = {
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"],
        "search": inputs["search_text"]
    }
    
    # Determine which attributes to include
    included_attrs = inputs["included_attributes"]
    
    # Build the URL with query parameters - use countries endpoint at root
    url = f"{base_url}/countries"
    
    # Make the request with the provided credential
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise exception for unsuccessful HTTP responses
        
        data = response.json()
        
        # If the response is empty (successful but no results), return None
        if not data:
            return None
        
        # Filter to only include requested attributes
        filtered_data = []
        for country in data:
            filtered_country = {}
            for attr in included_attrs:
                if attr in country:
                    filtered_country[attr] = country[attr]
            filtered_data.append(filtered_country)
        
        return filtered_data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")