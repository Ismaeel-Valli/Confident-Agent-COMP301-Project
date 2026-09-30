import requests

def solve(inputs):
    """
    Look up countries by exact match on their calling code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - 'value': The calling code to match exactly (string)
            - 'credential': Caller-supplied credential for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com/v5"
    
    # Construct the API endpoint for calling code lookup
    url = f"{base_url}/country/iso2ByName?fields=callingCodes&name={inputs['value']}"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Check for unsuccessful HTTP responses
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        
        # Decode the JSON response
        data = response.json()
        
        # Return None for successful empty response
        if not data:
            return None
        
        return data
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")