import requests

def solve(inputs):
    """
    Look up countries by exact match on their subregion using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The subregion to match exactly
            - result_limit: Maximum number of results
            - excluded_attributes: List of country attributes to exclude from response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build the request URL with subregion parameter
    url = f"{base_url}/v5/subregion/{inputs['value']}"
    
    # Set up headers with credential
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    params = {
        "limit": inputs["result_limit"]
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        # Raise exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Decode JSON response
        data = response.json()
        
        # Filter out excluded attributes if any
        if inputs["excluded_attributes"]:
            filtered_data = []
            for country in data:
                filtered_country = {k: v for k, v in country.items() 
                                  if k not in inputs["excluded_attributes"]}
                filtered_data.append(filtered_country)
            return filtered_data
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")