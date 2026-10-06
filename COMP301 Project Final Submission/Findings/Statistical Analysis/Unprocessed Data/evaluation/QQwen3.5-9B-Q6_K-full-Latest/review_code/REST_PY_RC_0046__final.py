import requests

def solve(inputs):
    """
    Search country names using REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - result_limit (int): Maximum number of results to return.
            - results_to_skip (int): Number of results to skip.
            - excluded_attributes (list): Attributes to exclude from response.
            - search_text (str): Search term for country names.
            - credential (str): Caller-supplied authentication token.
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com/v5"
    endpoint = "/countries"
    
    params = {
        "name": inputs["search_text"],
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    url = f"{base_url}{endpoint}"
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # Filter out excluded attributes if any
        if inputs["excluded_attributes"]:
            filtered_data = []
            for country in data:
                filtered_country = {k: v for k, v in country.items() 
                                   if k not in inputs["excluded_attributes"]}
                filtered_data.append(filtered_country)
            return filtered_data
        
        return data if data else None
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")