import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - results_to_skip (int): Number of results to skip (pagination offset)
            - credential (str): Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build the request URL with pagination parameter
    url = f"{base_url}/v5/countries?skip={inputs['results_to_skip']}"
    
    # Prepare headers with the credential
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Check for unsuccessful HTTP response
        if not response.ok:
            raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
        
        # Decode the JSON response
        data = response.json()
        
        # Return None for successful empty response
        if len(data) == 0:
            return None
        
        return data
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")