import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - excluded_attributes (list): Attributes to exclude from response
            - search_text (str): Search term for country names
            - credential (str): Caller-supplied authentication token
    
    Returns:
        dict or None: Decoded JSON response, or None if empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com/v5.1"
    
    # Build query parameters
    params = {}
    
    if inputs.get("search_text"):
        params["name"] = inputs["search_text"]
    
    if inputs.get("excluded_attributes"):
        # REST Countries v5 uses 'fields' parameter to specify included fields
        exclude_list = ",".join(inputs["excluded_attributes"])
        params["fields"] = exclude_list
    
    # Use the provided credential in Authorization header
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    try:
        response = requests.get(
            base_url,
            params=params,
            headers=headers
        )
        
        if response.status_code != 200:
            raise Exception(f"HTTP error: {response.status_code} - {response.text}")
        
        data = response.json()
        
        # Return None for successful empty response
        if not data:
            return None
        
        return data
    
    except requests.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")