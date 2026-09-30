import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Parameters:
        inputs (dict): Dictionary containing:
            - results_to_skip (int): Number of results to skip.
            - credential (str): Caller-supplied credential with necessary permissions.
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    url = f"{base_url}/v5/countries?skip={inputs['results_to_skip']}"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    data = response.json()
    return data