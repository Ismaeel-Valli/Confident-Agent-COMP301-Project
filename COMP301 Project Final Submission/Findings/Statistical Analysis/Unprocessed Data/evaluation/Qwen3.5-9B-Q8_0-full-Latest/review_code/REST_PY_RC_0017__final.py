import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5, excluding specified attributes.
    
    Args:
        inputs (dict): Dictionary containing:
            - excluded_attributes (list): List of country attributes to exclude.
            - credential (str): Caller-supplied credential with necessary permissions.
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    endpoint = "/v5/countries"
    
    # Build query parameters
    params = {}
    if inputs.get("excluded_attributes"):
        params["exclude"] = ",".join(inputs["excluded_attributes"])
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    url = base_url + endpoint
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        # Return None for successful empty response
        if not data:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")