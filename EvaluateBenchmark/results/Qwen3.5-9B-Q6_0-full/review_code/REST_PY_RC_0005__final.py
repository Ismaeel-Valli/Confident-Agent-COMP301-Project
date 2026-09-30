import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Contains 'result_limit' and 'credential'.
        
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    result_limit = inputs["result_limit"]
    credential = inputs["credential"]
    
    # Construct the API endpoint with query parameters
    params = {
        "limit": result_limit,
        "page": 1
    }
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(
        base_url + "/v5/countries",
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