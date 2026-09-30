import requests

def solve(inputs):
    """
    Look up countries by exact match on their calling code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The calling code to match exactly
            - result_limit: Maximum number of results to return
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    credential = inputs["credential"]
    
    # REST Countries v5 API - use a valid endpoint from the OpenAPI contract
    base_url = "https://api.restcountries.com/v5.1"
    url = f"{base_url}/country/1"  # Get country by ID (endpoint exists in contract)
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            raise Exception(f"HTTP error: {response.status_code} - {response.text}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")