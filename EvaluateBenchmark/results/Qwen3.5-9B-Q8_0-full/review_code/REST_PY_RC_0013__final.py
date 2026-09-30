import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - included_attributes (list): List of country attributes to include
            - credential (str): Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    endpoint = "/v5/countries"
    
    # Build query parameters
    params = {}
    if inputs.get("included_attributes"):
        params["attributes"] = ",".join(inputs["included_attributes"])
    
    # Prepare request with credential in headers
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    url = base_url + endpoint
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx/5xx)
        
        data = response.json()
        
        # Return None for successful empty response
        if not data:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")