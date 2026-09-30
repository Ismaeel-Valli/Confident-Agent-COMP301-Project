import requests

def solve(inputs):
    """
    Retrieves one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'results_to_skip' (int): Number of results to skip.
            - 'credential' (str): Caller-supplied credential (e.g., API key).
    
    Returns:
        dict or None: Decoded JSON response. Returns None for a successful empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://restcountries.com/v5.1"
    endpoint = "/data/countries"
    
    params = {
        "skip": inputs["results_to_skip"],
        "limit": 10  # Retrieve one page (assuming 10 items per page as a standard)
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(f"{base_url}{endpoint}", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for a successful empty response
    if not data:
        return None
    
    return data