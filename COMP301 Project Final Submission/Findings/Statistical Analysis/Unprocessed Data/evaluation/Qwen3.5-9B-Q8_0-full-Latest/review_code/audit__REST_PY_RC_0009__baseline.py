import requests

def solve(inputs):
    """
    Retrieves one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'results_to_skip' (int): Number of results to skip.
            - 'credential' (str): Caller-supplied credential (e.g., API key).
    
    Returns:
        dict or None: Decoded JSON response. Returns None if the response is empty but successful.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://restcountries.com/v5.1"
    endpoint = "/data/countries"
    
    params = {
        "skip": inputs["results_to_skip"],
        "limit": 10,  # Retrieve one page (assuming 10 items per page as a standard)
        "fields": ["name", "cca2", "cca3", "capital", "region", "subregion"]  # Example fields; adjust if needed
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    url = f"{base_url}{endpoint}"
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP request failed with status code: {response.status_code}. Response body: {response.text}")
    
    data = response.json()
    
    # Return None for a successful empty response
    if not data:
        return None
    
    return data