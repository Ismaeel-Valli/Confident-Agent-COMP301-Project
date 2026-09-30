import requests

def solve(inputs):
    """
    Look up countries by exact match on their subregion using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The subregion to match exactly
            - included_attributes: List of attributes to return for each country
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response. None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com/v5"
    subregion = inputs["value"]
    credential = inputs["credential"]
    included_attributes = inputs.get("included_attributes", [])
    
    # Build query parameters
    params = {
        "subregion": subregion,
        "credential": credential
    }
    
    if included_attributes:
        params["fields"] = ",".join(included_attributes)
    
    url = f"{base_url}/countries"
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Return None for successful empty response (empty list)
        if not data:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")