import requests

def solve(inputs):
    """
    Retrieves one page of countries from REST Countries v5 API using provided credentials.
    
    Args:
        inputs (dict): Contains 'results_to_skip' and 'credential'.
        
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://restcountries.com/v5"
    endpoint = "/geonames"  # Using geonames as a representative endpoint for countries data
    
    results_to_skip = inputs.get("results_to_skip", 0)
    credential = inputs.get("credential")
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    params = {
        "skip": results_to_skip,
        "limit": 1
    }
    
    response = requests.get(f"{base_url}/{endpoint}", headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP Error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
        
    return data