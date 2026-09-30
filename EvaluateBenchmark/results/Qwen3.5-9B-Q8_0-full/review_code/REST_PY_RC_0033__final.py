import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return
            - excluded_attributes (list): List of country attributes to exclude
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    endpoint = "/v5/countries"
    
    params = {
        "limit": inputs["result_limit"],
        "credential": inputs["credential"]
    }
    
    # Build query string for excluded attributes if any
    if inputs["excluded_attributes"]:
        excluded_str = ",".join(inputs["excluded_attributes"])
        params["exclude"] = excluded_str
    
    url = f"{base_url}{endpoint}"
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Return None for successful empty response
        if not data:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")